from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user
from main import main

@main.route('/')
def home():
    """Landing page for the application."""
    if current_user.is_authenticated:
        if current_user.profession == 'Farmer':
            return redirect(url_for('farmer.dashboard'))
        else:  # Agent
            return redirect(url_for('agent.dashboard'))
    return render_template('main/index.html', title='Welcome to AgriSure')

@main.route('/about')
def about():
    """About page with company information."""
    return render_template('main/about.html', title='About AgriSure')

@main.route('/customer-care', methods=['GET', 'POST'])
def customer_care():
    """Customer care page with support form."""
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        
        # In a real app, save the support query or send an email
        # For now, just show a success message
        flash('Your message has been received. Our team will contact you shortly!', 'success')
        return redirect(url_for('main.customer_care'))
    
    return render_template('main/customer_care.html', title='Customer Care')