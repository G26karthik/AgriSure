
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('insurance-form');
    const resultArea = document.getElementById('result-area');
    const errorArea = document.getElementById('error-area');
    const calculateBtn = document.getElementById('calculate-btn');
    const spinner = calculateBtn.querySelector('.spinner-border');

    // Form Submission Handler
    form.addEventListener('submit', function(event) {
        event.preventDefault(); // Prevent default form submission
        clearResults();
        showSpinner(true);

        const formData = new FormData(form);

        fetch('/calculate', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (!response.ok) {
                // Try to parse error message from server if available
                return response.json().then(err => { throw new Error(err.error || `HTTP error! status: ${response.status}`) });
            }
            return response.json();
        })
        .then(data => {
            if (data.error) {
                showError(data.error);
            } else {
                displayResults(data);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showError(`Calculation failed: ${error.message}. Please check inputs or try again later.`);
        })
        .finally(() => {
            showSpinner(false);
        });
    });

    // --- Helper Functions ---
    function showSpinner(show) {
        if (show) {
            spinner.classList.remove('d-none');
            calculateBtn.disabled = true;
        } else {
            spinner.classList.add('d-none');
            calculateBtn.disabled = false;
        }
    }

    function clearResults() {
        resultArea.classList.add('d-none');
        errorArea.classList.add('d-none');
        errorArea.textContent = '';
        document.getElementById('risk-level').textContent = '';
        document.getElementById('insurance-cover').textContent = '';
        document.getElementById('weather-info').textContent = '';
        document.getElementById('risk-reasons').textContent = '';
        document.getElementById('insurance-reason').textContent = '';
         // Remove previous risk classes
        document.getElementById('risk-level').classList.remove('risk-high', 'risk-medium', 'risk-low');
    }

    function showError(message) {
        errorArea.textContent = message;
        errorArea.classList.remove('d-none');
    }

    function displayResults(data) {
        const riskLevelEl = document.getElementById('risk-level');
        riskLevelEl.textContent = `Risk Level: ${data.risk_level}`;
        // Add class based on risk level for styling
        riskLevelEl.classList.add(`risk-${data.risk_level.toLowerCase()}`);


        document.getElementById('insurance-cover').textContent = `Recommended Insurance Cover: ${data.insurance_cover}`;
        document.getElementById('weather-info').textContent = data.weather_info || '';
        document.getElementById('risk-reasons').textContent = `Risk Factors: ${Array.isArray(data.risk_reasons) ? data.risk_reasons.join(', ') : data.risk_reasons}`;
        document.getElementById('insurance-reason').textContent = data.insurance_reason || '';

        resultArea.classList.remove('d-none');
    }


    // --- Optional: Web Speech API for Voice Input ---
    const voiceInputBtn = document.getElementById('voice-input-btn');
    const cropTypeInput = document.getElementById('crop_type');
    const locationInput = document.getElementById('location');
    const landAreaInput = document.getElementById('land_area');

    // Check if SpeechRecognition is supported
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    let recognition;

    if (SpeechRecognition) {
        recognition = new SpeechRecognition();
        recognition.continuous = false; // Process single utterance
        recognition.lang = 'en-US'; // Set language
        recognition.interimResults = false; // Get final result
        recognition.maxAlternatives = 1; // Get the best match

        voiceInputBtn.addEventListener('click', () => {
            try {
                recognition.start();
                voiceInputBtn.textContent = '👂'; // Indicate listening
                voiceInputBtn.disabled = true;
                showError(''); // Clear previous errors
            } catch(e) {
                console.error("Speech recognition already started or error starting:", e);
                 showError("Could not start voice recognition. Is microphone permission granted?");
                 voiceInputBtn.textContent = '🎤';
                 voiceInputBtn.disabled = false;
            }
        });

        recognition.onresult = (event) => {
            const speechResult = event.results[0][0].transcript.toLowerCase();
            console.log('Speech recognized:', speechResult);

            // Basic parsing (very simple, needs improvement for robustness)
            // Example commands:
            // "Crop wheat location Pune area 5 acres"
            // "Set crop to rice"
            // "Location Delhi"
            // "Area 10.5"

            let filledSomething = false;

            // Try to extract crop type
            const cropMatch = speechResult.match(/crop (type |is |to )?([a-zA-Z\s]+)(?= location| area|$)/);
            if (cropMatch && cropMatch[2]) {
                cropTypeInput.value = cropMatch[2].trim();
                filledSomething = true;
            }

            // Try to extract location
            const locationMatch = speechResult.match(/location (is |to )?([a-zA-Z\s,]+)(?= area|$)/);
             if (locationMatch && locationMatch[2]) {
                locationInput.value = locationMatch[2].trim();
                 filledSomething = true;
            }

            // Try to extract land area
            const areaMatch = speechResult.match(/(area|acres) (is |to )?([\d.]+)/);
             if (areaMatch && areaMatch[3]) {
                landAreaInput.value = areaMatch[3].trim();
                 filledSomething = true;
            }

            if (!filledSomething) {
                 showError(`Could not parse voice input: "${speechResult}". Try commands like "Crop wheat location Pune area 5".`);
            }
        };

        recognition.onspeechend = () => {
            recognition.stop();
            voiceInputBtn.textContent = '🎤';
            voiceInputBtn.disabled = false;
        };

        recognition.onerror = (event) => {
            console.error('Speech recognition error:', event.error);
             showError(`Voice recognition error: ${event.error}. Please ensure microphone access is allowed.`);
            voiceInputBtn.textContent = '🎤';
            voiceInputBtn.disabled = false;
        };

        recognition.onnomatch = (event) => {
             showError("Sorry, I didn't recognize that. Please try again.");
             voiceInputBtn.textContent = '🎤';
             voiceInputBtn.disabled = false;
        }


    } else {
        // Hide the button if API is not supported
        voiceInputBtn.style.display = 'none';
        console.warn("Web Speech API not supported in this browser.");
    }

});
