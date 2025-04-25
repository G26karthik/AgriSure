import os
from flask import Flask, render_template
from flask_login import LoginManager
from werkzeug.utils import secure_filename
from flask_wtf.csrf import CSRFProtect
from models import User
from config import Config

# Create the Flask application
app = Flask(__name__)
app.config.from_object(Config)
app.config['SECRET_KEY'] = 'your-secret-key-here'  # Add a secret key for security
app.config['WTF_CSRF_ENABLED'] = True  # Enable CSRF protection

# Initialize CSRF protection
csrf = CSRFProtect(app)

# Configure upload folder
upload_folder = app.config['UPLOAD_FOLDER']
os.makedirs(upload_folder, exist_ok=True)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

# Import blueprints
from main import main, routes as main_routes
from auth import auth, routes as auth_routes
from farmer import farmer, routes as farmer_routes
from agent import agent, routes as agent_routes

# Register blueprints
app.register_blueprint(main)
app.register_blueprint(auth)
app.register_blueprint(farmer)
app.register_blueprint(agent)

# Register error handlers
@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html', title='Page Not Found'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('errors/500.html', title='Server Error'), 500

if __name__ == '__main__':
    app.run(debug=True)
