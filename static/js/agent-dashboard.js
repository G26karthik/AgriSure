// Agent dashboard task submission functionality
document.addEventListener('DOMContentLoaded', function() {
    const uploadModal = document.getElementById('uploadModal');
    const uploadForm = document.getElementById('upload-form');
    const modalTaskIdInput = document.getElementById('modal-task-id');
    const submitUploadBtn = document.getElementById('submit-upload');
    let isSubmitting = false;
    
    // Set the task ID when opening the modal
    document.querySelectorAll('.upload-btn').forEach(button => {
        button.addEventListener('click', function() {
            const taskId = this.getAttribute('data-task-id');
            modalTaskIdInput.value = taskId;
            
            // Reset form and button state when opening modal
            uploadForm.reset();
            submitUploadBtn.disabled = false;
            submitUploadBtn.innerHTML = 'Submit';
            isSubmitting = false;
        });
    });
    
    // Handle form submission
    submitUploadBtn.addEventListener('click', function() {
        // Prevent multiple submissions
        if (isSubmitting) {
            return;
        }
        
        const taskId = modalTaskIdInput.value;
        const fileInput = document.getElementById('crop_images');
        
        if (!fileInput.files.length) {
            alert('Please select at least one image to upload.');
            return;
        }
        
        // Set submission flag and update button
        isSubmitting = true;
        this.disabled = true;
        this.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Uploading...';
        
        // Create form data
        const formData = new FormData(uploadForm);
        
        // Submit the form
        fetch(`/agent/submit-task/${taskId}`, {
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
                // Success - close modal first, then show message
                const modalInstance = bootstrap.Modal.getInstance(uploadModal);
                modalInstance.hide();
                setTimeout(() => {
                    alert('Task submitted successfully!');
                    window.location.reload();
                }, 500);
            } else {
                // API returned an error
                throw new Error(data.error || 'Failed to submit task.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert(`Error: ${error.message || 'An error occurred while submitting the task. Please try again.'}`);
            
            // Reset submission state
            isSubmitting = false;
            this.disabled = false;
            this.innerHTML = 'Submit';
        });
    });
});
