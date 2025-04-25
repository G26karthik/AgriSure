from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from farmer import farmer
from models import user_data, insurance_data, find_plan_by_id, HARDCODED_PLANS
import os
from datetime import datetime
import json
import requests

# Helper function for recommending insurance plans
def recommend_plan(crop_name, location, sowing_date, crop_term):
    """Returns recommended plans based on crop details."""
    # For now, just return the hardcoded plans based on term
    return HARDCODED_PLANS.get(crop_term, [])

# Decorator to check if the current user is a farmer
def farmer_required(f):
    @login_required
    def decorated_function(*args, **kwargs):
        if current_user.profession != 'Farmer':
            flash('Access denied: You must be logged in as a Farmer to view this page.', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__  # Preserve original function name
    return decorated_function

@farmer.route('/dashboard')
@farmer_required
def dashboard():
    """Farmer dashboard with access to all features."""
    # Get user name from user_data dictionary
    user_info = user_data.get(current_user.id, {})
    return render_template('farmer/dashboard.html', 
                           user_name=user_info.get('name', 'Farmer'),
                           title='Farmer Dashboard')

@farmer.route('/risk-estimator')
@farmer_required
def insurance_estimator():
    """Risk estimation tool for farmers."""
    return render_template('farmer/insurance_estimator.html', title='Risk Estimator')

@farmer.route('/insurance-plans', methods=['GET', 'POST'])
@farmer_required
def insurance_plans():
    """Browse and select insurance plans."""
    recommended_plans = []
    form_data = {}
    
    if request.method == 'POST':
        # Store form data to repopulate the form
        form_data = request.form.to_dict()
        crop_name = form_data.get('crop_name')
        location = form_data.get('location')
        sowing_date = form_data.get('sowing_date')
        crop_term = form_data.get('crop_term')

        if not all([crop_name, location, sowing_date, crop_term]):
            flash('Please fill in all fields.', 'warning')
        else:
            # Find plans based on term and additional criteria
            recommended_plans = recommend_plan(crop_name, location, sowing_date, crop_term)
            if not recommended_plans:
                flash(f'No specific plans found for {crop_term} term based on current rules. Showing general options for the term.', 'info')
                recommended_plans = HARDCODED_PLANS.get(crop_term, [])

    return render_template('farmer/insurance_plans.html', 
                          recommended_plans=recommended_plans, 
                          form_data=form_data,
                          title='Insurance Plans')

@farmer.route('/select-plan/<plan_id>')
@farmer_required
def select_plan(plan_id):
    """Select a plan and proceed to document upload."""
    plan = find_plan_by_id(plan_id)
    if not plan:
        flash('Invalid plan selected.', 'danger')
        return redirect(url_for('farmer.insurance_plans'))
    
    # Store the selected plan in session if needed
    # session['selected_plan'] = plan_id
    
    return redirect(url_for('farmer.upload_docs', plan_id=plan_id))

@farmer.route('/upload-documents/<plan_id>', methods=['GET', 'POST'])
@farmer_required
def upload_docs(plan_id):
    """Upload required documents for the selected plan."""
    plan = find_plan_by_id(plan_id)
    if not plan:
        flash('Invalid plan selected.', 'danger')
        return redirect(url_for('farmer.insurance_plans'))
    
    if request.method == 'POST':
        # Get uploads directory from config
        upload_folder = os.path.join('uploads', current_user.id, plan_id)
        os.makedirs(upload_folder, exist_ok=True)
        
        # Placeholder for file paths
        document_paths = {}
        
        # Process each required document
        required_docs = ['passbook_doc', 'pahani_doc', 'one_b_doc', 'crop_image']
        for doc_name in required_docs:
            if doc_name not in request.files:
                flash(f'Missing required document: {doc_name}', 'danger')
                return redirect(request.url)
            
            file = request.files[doc_name]
            if file.filename == '':
                flash(f'No selected file for {doc_name}', 'danger')
                return redirect(request.url)
            
            if file:
                filename = secure_filename(file.filename)
                file_path = os.path.join(upload_folder, filename)
                # file.save(file_path)  # Commented out for demo
                document_paths[doc_name] = file_path
        
        # Verify geo-tag for crop image (placeholder)
        # lat = request.form.get('latitude')
        # lon = request.form.get('longitude')
        # if lat and lon:
        #     verified = True  # placeholder for actual verification
        # else:
        #     verified = False
        verified = True  # For demo purposes
        
        if verified:
            # Store uploaded document paths for later
            # session['document_paths'] = document_paths
            flash('Documents uploaded successfully!', 'success')
            return redirect(url_for('farmer.payment', plan_id=plan_id))
        else:
            flash('Location verification failed. Please ensure location is enabled when taking crop photos.', 'danger')
    
    return render_template('farmer/upload_documents.html', 
                          plan_id=plan_id, 
                          plan=plan,
                          title='Upload Documents')

@farmer.route('/payment/<plan_id>', methods=['GET', 'POST'])
@farmer_required
def payment(plan_id):
    """Mock payment processing for the selected insurance plan."""
    plan = find_plan_by_id(plan_id)
    if not plan:
        flash('Invalid plan selected.', 'danger')
        return redirect(url_for('farmer.insurance_plans'))
    
    if request.method == 'POST':
        # Process payment (mock)
        receipt_id = f"RCPT-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        # Store the insurance in user's records
        store_insurance(current_user.id, plan, receipt_id)
        
        flash('Payment successful! Your insurance is now active.', 'success')
        return redirect(url_for('farmer.my_insurances'))
    
    return render_template('farmer/payment.html', 
                          plan_id=plan_id,
                          plan=plan,
                          title='Payment')

@farmer.route('/my-insurances')
@farmer_required
def my_insurances():
    """View all active insurance policies."""
    # Retrieve user's insurance policies
    user_insurances = insurance_data.get(current_user.id, [])
    
    # If no insurance data found, add a sample one for demo purposes
    if not user_insurances:
        from models import HARDCODED_PLANS
        sample_plan = HARDCODED_PLANS['Mid'][0]  # Use the first mid-term plan
        user_insurances = [{
            'plan_name': sample_plan['name'],
            'premium_paid': sample_plan['premium'],
            'coverage': sample_plan['coverage'],
            'purchase_date': '2025-01-15',
            'receipt_id': 'RCPT-20250115001',
            'documents': {}
        }]
        insurance_data[current_user.id] = user_insurances
    
    return render_template('farmer/my_insurances.html', 
                          insurances=user_insurances,
                          title='My Insurances')

@farmer.route('/calculate-risk', methods=['POST'])
@farmer_required
def calculate_risk():
    """API endpoint for risk estimation calculation."""
    try:
        data = request.form
        crop_type = data.get('crop_type', 'Unknown Crop')
        sowing_date = data.get('sowing_date', '')
        location = data.get('location', 'Unknown Location')
        land_area = data.get('land_area', '0')

        # Basic validation
        if not all([crop_type, sowing_date, location, land_area]):
            return jsonify({'error': 'Missing form data.'}), 400

        # 1. Get Weather (placeholder)
        weather_data = {
            'temperature': 28, 
            'weather_descriptions': ['Partly cloudy'],
            'humidity': 65
        }

        # 2. Estimate Risk (simplified for demo)
        risk_level = "Medium"
        risk_reasons = ["Based on crop type and season", "Historical weather patterns"]
        
        # 3. Suggest Insurance
        try:
            area = float(land_area)
            rate_per_acre = 3000 if risk_level == "Medium" else (4500 if risk_level == "High" else 1500)
            total_cover = rate_per_acre * area
            insurance_cover = f"₹{total_cover:,.0f}"
            insurance_reason = f"Based on {risk_level} risk for {area} acres."
        except ValueError:
            insurance_cover = "₹0"
            insurance_reason = "Invalid land area input."

        result = {
            'risk_level': risk_level,
            'risk_reasons': risk_reasons,
            'insurance_cover': insurance_cover,
            'insurance_reason': insurance_reason,
            'weather_info': f"Weather in {location}: {weather_data.get('temperature')}°C, {weather_data.get('weather_descriptions')[0]}, Humidity: {weather_data.get('humidity')}%"
        }
        return jsonify(result)

    except Exception as e:
        print(f"Error in /calculate-risk route: {e}")
        return jsonify({'error': 'An internal server error occurred.'}), 500

# --- Helper Functions ---

def recommend_plan(crop_name, location, sowing_date, crop_term):
    """Recommends insurance plans based on input criteria."""
    print(f"Recommend plan called with: {crop_name}, {location}, {sowing_date}, {crop_term}")
    term_plans = HARDCODED_PLANS.get(crop_term, [])
    
    # For now, just return plans matching the term
    # Future: Add filtering by crop type, risk level, etc.
    return term_plans

def store_insurance(user_id, plan_details, receipt_id):
    """Store insurance policy details in user's record."""
    new_insurance = {
        'plan_name': plan_details.get('name', 'Unknown Plan'),
        'premium_paid': plan_details.get('premium', 'N/A'),
        'coverage': plan_details.get('coverage', 'N/A'),
        'purchase_date': datetime.now().strftime('%Y-%m-%d'),
        'receipt_id': receipt_id,
        'documents': {}  # Store paths or references to uploaded docs
    }
    
    if user_id in insurance_data:
        insurance_data[user_id].append(new_insurance)
    else:
        insurance_data[user_id] = [new_insurance]
    return True

@farmer.route('/loan-services')
@farmer_required
def loan_services():
    return render_template('farmer/loan_services.html', title='Loan Services')

@farmer.route('/loan-document-upload')
@farmer_required
def loan_document_upload():
    return render_template('farmer/loan_document_upload.html', title='Loan Document Upload')

@farmer.route('/loan-application-submitted')
@farmer_required
def loan_application_submitted():
    flash('Your loan application and documents have been submitted successfully!', 'success')
    return redirect(url_for('farmer.loan_services'))

@farmer.route('/subsidies')
@farmer_required
def subsidies():
    return render_template('farmer/subsidies.html', title='Subsidies')

@farmer.route('/my-profile', methods=['GET', 'POST'])
@farmer_required
def my_profile():
    insurances = [
        {'id': 'AGRI-2024-105', 'crop': 'Rice', 'term': 'Short', 'start_date': '2024-06-01', 'end_date': '2024-11-30', 'status': 'Active'},
        {'id': 'AGRI-2023-088', 'crop': 'Wheat', 'term': 'Mid', 'start_date': '2023-11-01', 'end_date': '2024-04-30', 'status': 'Expired'},
        {'id': 'AGRI-2023-015', 'crop': 'Cotton', 'term': 'Long', 'start_date': '2023-05-15', 'end_date': '2024-01-15', 'status': 'Expired'}
    ]
    return render_template('farmer/my_profile.html', insurances=insurances, title='My Profile')

@farmer.route('/file-claim', methods=['POST'])
@farmer_required
def file_claim():
    policy_id = request.form.get('policy_id')
    loss_description = request.form.get('loss_description')
    files = request.files.getlist('crop_images')
    errors = []
    if not policy_id or not loss_description:
        errors.append('Please fill all required fields.')
    if not files or len(files) == 0:
        errors.append('Please upload at least one image.')
    if len(files) > 5:
        errors.append('You can upload a maximum of 5 images.')
    allowed_ext = {'jpg', 'jpeg', 'png'}
    for f in files:
        if '.' not in f.filename or f.filename.split('.')[-1].lower() not in allowed_ext:
            errors.append(f'File {f.filename} is not a valid image.')
        if hasattr(f, 'content_length') and f.content_length and f.content_length > 5 * 1024 * 1024:
            errors.append(f'File {f.filename} exceeds 5MB size limit.')
    if errors:
        for err in errors:
            flash(err, 'danger')
        return redirect(url_for('farmer.my_profile'))
    flash('Your insurance claim has been submitted successfully!', 'success')
    return redirect(url_for('farmer.my_profile'))

@farmer.route('/update-profile', methods=['POST'])
@farmer_required
def update_profile():
    """Update farmer profile information."""
    if request.method == 'POST':
        name = request.form.get('name')
        address = request.form.get('address')
        dob = request.form.get('dob')
        
        # Update user data in memory
        if current_user.id in user_data:
            user_data[current_user.id]['name'] = name
            user_data[current_user.id]['address'] = address
            user_data[current_user.id]['dob'] = dob
            flash('Profile updated successfully!', 'success')
        else:
            flash('Error updating profile. Please try again.', 'danger')
            
    return redirect(url_for('farmer.my_profile'))