from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import datetime

# --- In-Memory Data Storage (Global Variables - Data lost on restart) ---
# users format: { 'phone_number': {'password_hash': '...', 'id': 'phone_number', 'profession': '...'} }
users = {}
# user_data format: { 'phone_number': {'name': '...', 'address': '...', 'dob': ..., 'district': ...} }
user_data = {}
# insurance_data format: { 'phone_number': [{'plan_id': ..., 'plan_name': ..., ...}, ...] }
insurance_data = {}
# Placeholder for agent tasks (could be a list of dicts)
agent_tasks = {} # { 'agent_phone': [ { 'task_id': ..., 'farmer_name': ..., ... } ] }
# Placeholder for claims
claims_data = {} # { 'user_phone': [ { 'claim_id': ..., 'insurance_id': ..., ... } ] }


# --- User Class (Simple Class for Flask-Login) ---
class User(UserMixin):
    def __init__(self, id, profession='Farmer'): # Default profession or get from users dict
        self.id = id # Use phone number as ID
        # Fetch profession safely from the global users dictionary
        user_info = users.get(id, {})
        self.profession = user_info.get('profession', profession)

    @staticmethod
    def get(user_id):
        """Needed by Flask-Login: Get user by ID (phone number)."""
        if user_id in users:
            # Pass the correct profession when creating the User instance
            user_info = users.get(user_id, {})
            return User(user_id, profession=user_info.get('profession', 'Farmer'))
        return None

    @staticmethod
    def register(name, phone_number, password, profession, address=None, dob=None, district=None):
        """Registers a new user in the in-memory dictionary."""
        if phone_number in users:
            return False, "Phone number already registered."

        password_hash = generate_password_hash(password)
        users[phone_number] = {
            'id': phone_number,
            'password_hash': password_hash,
            'profession': profession
        }
        user_data[phone_number] = {
            'name': name,
            'address': address,
            'dob': dob,
            'district': district if profession == 'Agent' else None
        }
        insurance_data[phone_number] = [] # Initialize empty insurance list for the user
        claims_data[phone_number] = [] # Initialize empty claims list
        print(f"User registered (in-memory): {phone_number}, Profession: {profession}") # Debugging
        return True, "Registration successful. Please login."

    @staticmethod
    def authenticate(phone_number, password, profession_login):
        """Authenticates a user against the in-memory dictionary."""
        user_info = users.get(phone_number)
        # Check if user exists, password matches, AND profession matches
        if user_info and \
           check_password_hash(user_info.get('password_hash', ''), password) and \
           user_info.get('profession') == profession_login:
            # Pass the correct profession when creating the User instance
            return User(phone_number, profession=user_info['profession'])
        return None

    # Flask-Login integration requires this method if UserMixin is used
    def get_id(self):
           return str(self.id) # Return as string


# --- Hardcoded Insurance Plans (Moved here for better organization) ---
HARDCODED_PLANS = {
    'Short': [
        {'id': 'S1', 'name': 'Basic Kharif Cover', 'premium': '₹1,200', 'coverage': '₹25,000', 'duration': '3-4 Months', 'risk_suitability': ['Low', 'Medium'], 'crops': ['Rice', 'Soybean']},
        {'id': 'S2', 'name': 'Medium Kharif Secure', 'premium': '₹1,800', 'coverage': '₹40,000', 'duration': '3-4 Months', 'risk_suitability': ['Medium', 'High'], 'crops': ['Cotton', 'Maize']},
        {'id': 'S3', 'name': 'Quick Veggie Guard', 'premium': '₹1,000', 'coverage': '₹20,000', 'duration': '2-3 Months', 'risk_suitability': ['Low'], 'crops': ['Tomato', 'Onion']},
        {'id': 'S4', 'name': 'Monsoon Pulse Shield', 'premium': '₹1,400', 'coverage': '₹30,000', 'duration': '3 Months', 'risk_suitability': ['Medium'], 'crops': ['Moong', 'Urad']},
        {'id': 'S5', 'name': 'Rabi Weather Shield', 'premium': '₹1,500', 'coverage': '₹35,000', 'duration': '4 Months', 'risk_suitability': ['Medium'], 'crops': ['Mustard', 'Gram']},
    ],
    'Mid': [
        {'id': 'M1', 'name': 'Standard Mid Term Protect', 'premium': '₹2,800', 'coverage': '₹60,000', 'duration': '6 Months', 'risk_suitability': ['Low', 'Medium'], 'crops': ['Sugarcane', 'Banana']},
        {'id': 'M2', 'name': 'Enhanced Growth Secure', 'premium': '₹3,500', 'coverage': '₹75,000', 'duration': '5-7 Months', 'risk_suitability': ['Medium', 'High'], 'crops': ['Turmeric', 'Ginger']},
        {'id': 'M3', 'name': 'Orchard Bloom Guard', 'premium': '₹4,000', 'coverage': '₹90,000', 'duration': '6-8 Months', 'risk_suitability': ['Medium'], 'crops': ['Mango', 'Guava']},
        {'id': 'M4', 'name': 'Cotton Boll Protect', 'premium': '₹3,200', 'coverage': '₹70,000', 'duration': '6 Months', 'risk_suitability': ['High'], 'crops': ['Cotton']},
        {'id': 'M5', 'name': 'Extended Growth Plan', 'premium': '₹3,000', 'coverage': '₹65,000', 'duration': '5-6 Months', 'risk_suitability': ['Low', 'Medium'], 'crops': ['Pulses', 'Groundnut']},
   ],
    'Long': [
        {'id': 'L1', 'name': 'Annual Crop Shield', 'premium': '₹5,500', 'coverage': '₹120,000', 'duration': '1 Year', 'risk_suitability': ['Low', 'Medium'], 'crops': ['Plantation Crops', 'Coconut']},
        {'id': 'L2', 'name': 'Perennial Plant Guard', 'premium': '₹6,500', 'coverage': '₹150,000', 'duration': '1 Year', 'risk_suitability': ['Medium'], 'crops': ['Tea', 'Coffee', 'Rubber']},
        {'id': 'L3', 'name': 'Forestry Secure Plan', 'premium': '₹8,000', 'coverage': '₹180,000', 'duration': '1 Year+', 'risk_suitability': ['Medium', 'High'], 'crops': ['Timber', 'Bamboo']},
        {'id': 'L4', 'name': 'Vineyard Annual Cover', 'premium': '₹7,000', 'coverage': '₹160,000', 'duration': '1 Year', 'risk_suitability': ['High'], 'crops': ['Grapes']},
        {'id': 'L5', 'name': 'Farm Asset Annual Plan', 'premium': '₹7,500', 'coverage': '₹160,000', 'duration': '1 Year', 'risk_suitability': ['Medium', 'High'], 'crops': ['Mixed Farming', 'Arecanut']},
    ]
}

def find_plan_by_id(plan_id):
    """Finds a specific plan details from HARDCODED_PLANS by its ID."""
    for term in HARDCODED_PLANS:
        for plan in HARDCODED_PLANS[term]:
            if plan['id'] == plan_id:
                return plan
    return None
