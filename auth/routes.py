from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from auth import auth
from forms import LoginForm, RegistrationForm
from models import User
import datetime

@auth.route('/login', methods=['GET', 'POST'])
def login():
    """Handles user login for both Farmers and Agents."""
    if current_user.is_authenticated:
        if current_user.profession == 'Farmer':
            return redirect(url_for('farmer.dashboard'))
        else:  # Agent
            return redirect(url_for('agent.dashboard'))

    form = LoginForm()
    if form.validate_on_submit():
        phone_number = form.phone_number.data
        password = form.password.data
        profession = form.profession.data
        remember = form.remember_me.data

        user = User.authenticate(phone_number, password, profession)

        if user:
            login_user(user, remember=remember)
            
            # Add sample insurance data for demo purposes if this user doesn't have any yet
            if profession == 'Farmer' and phone_number not in insurance_data:
                from models import insurance_data, HARDCODED_PLANS
                sample_plan = HARDCODED_PLANS['Mid'][0]  # Use the first mid-term plan as example
                insurance_data[phone_number] = [{
                    'plan_name': sample_plan['name'],
                    'premium_paid': sample_plan['premium'],
                    'coverage': sample_plan['coverage'],
                    'purchase_date': '2025-01-15',
                    'receipt_id': 'RCPT-20250115001',
                    'documents': {}
                }]
            
            flash(f'Welcome back! You are now logged in as {profession}.', 'success')
            
            # Redirect based on profession
            if user.profession == 'Farmer':
                return redirect(url_for('farmer.dashboard'))
            else:  # Agent
                return redirect(url_for('agent.dashboard'))
        else:
            flash('Login failed. Please check your phone number, password, and profession.', 'danger')

    return render_template('auth/login.html', form=form, title='Login')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    """Handles user registration for both Farmers and Agents."""
    if current_user.is_authenticated:
        flash('You are already registered and logged in.', 'info')
        if current_user.profession == 'Farmer':
            return redirect(url_for('farmer.dashboard'))
        else:  # Agent
            return redirect(url_for('agent.dashboard'))

    form = RegistrationForm()
    if form.validate_on_submit():
        name = form.name.data
        phone_number = form.phone_number.data
        password = form.password.data
        profession = form.profession.data
        address = form.address.data
        
        # Format date as string if present, otherwise None
        dob = form.dob.data.strftime('%Y-%m-%d') if form.dob.data else None
        
        district = form.district.data if profession == 'Agent' else None

        success, message = User.register(
            name=name,
            phone_number=phone_number,
            password=password,
            profession=profession,
            address=address,
            dob=dob,
            district=district
        )

        if success:
            flash(f'Registration successful! You can now log in as a {profession}.', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash(f'Registration failed: {message}', 'danger')

    return render_template('auth/register.html', form=form, title='Register')

@auth.route('/logout')
@login_required
def logout():
    """Logs out the current user."""
    logout_user()
    flash('You have been successfully logged out.', 'info')
    return redirect(url_for('auth.login'))