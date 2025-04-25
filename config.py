import os

# Determine the absolute path of the directory containing config.py
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a-hard-to-guess-string-for-dev' # Change this!
    UPLOAD_FOLDER = os.path.join(basedir, 'uploads') # Folder for uploads
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf'} # Allowed file types
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024 # Optional: Limit upload size (e.g., 16MB)

    # Ensure the upload folder exists
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
