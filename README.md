
# AgriSure

AgriSure is a modern agricultural insurance and financial services platform designed to empower farmers and rural agents. It streamlines crop insurance enrollment, claim management, loan eligibility, and more—making financial security accessible, transparent, and fast for the people who feed the world.

---

## 1. Overview

**AgriSure** solves real problems for Indian farmers and rural agents:
- **Crop loss** from weather, pests, or disease can devastate a family. AgriSure makes insurance enrollment, claims, and payouts simple and fast.
- **Financial inclusion**: Farmers can check loan eligibility, upload documents, and access government subsidies—all in one place.
- **Agent empowerment**: Rural agents get dashboards to manage field tasks, verify claims, and help farmers on the ground.

The platform is built to be intuitive, mobile-friendly, and available in local languages.

---

## 2. Core Features

- **Farmer Dashboard**: One-stop panel for insurance, loans, subsidies, and profile management.
- **Insurance Plan Finder**: Enter crop details to get personalized insurance recommendations.
- **Digital Enrollment & Document Upload**: Apply for insurance or loans, upload required documents, and track status.
- **Risk Estimator**: Simple tool to estimate crop risk and suggest suitable plans.
- **Claims Management**: File claims, upload evidence, and track progress.
- **Agent Dashboard**: View assigned tasks, verify claims, and submit field reports.
- **Loan Services**: Check eligibility, upload documents, and track loan applications.
- **Subsidies & Alerts**: Access government/private subsidies and receive weather alerts.
- **Authentication**: Secure login/registration for both farmers and agents.

---

## 3. Architecture Overview

**Backend**:  
- Built with **Flask** (Python), using Blueprints for modular routing (`main`, `auth`, `farmer`, `agent`).
- **Flask-Login** for authentication/session management.
- **Flask-WTF** for secure forms and validation.
- **In-memory data storage** (dictionaries) for demo purposes; easily swappable for SQLAlchemy/DB.

**Frontend**:  
- **Jinja2** templates for dynamic HTML rendering.
- **Bootstrap 5** for responsive, mobile-first UI.
- **Font Awesome** for icons.
- **Custom JavaScript** for interactivity (form logic, dashboard widgets).

**Data Flow**:  
- User actions (register, login, apply, upload) trigger Flask routes.
- Data is validated via Flask-WTF forms.
- Templates render context-aware pages, with Bootstrap and JS for UX.
- File uploads are stored in a dedicated `uploads/` directory.

---

## 4. Backend Logic (Flask)

- **File Structure**:
  - `app.py`: App factory, blueprint registration, error handlers.
  - `models.py`: User model, in-memory data stores, insurance plan definitions.
  - `forms.py`: WTForms-based registration and login forms with custom validation.
  - `config.py`: App configuration (secret keys, upload folder, etc.).
  - `main/`, `auth/`, `farmer/`, `agent/`: Each as a Flask Blueprint with its own `routes.py`.

- **Routing**:
  - `/auth/login`, `/auth/register`: Handles both farmer and agent authentication.
  - `/farmer/dashboard`, `/agent/dashboard`: Role-based dashboards.
  - `/farmer/insurance-plans`, `/farmer/upload-documents/<plan_id>`, `/farmer/my-insurances`: Insurance workflows.
  - `/agent/verify-claim/<claim_id>`, `/agent/completed-tasks`: Agent claim verification and history.

- **Database/Models**:
  - Uses Python dictionaries for users, insurance data, agent tasks, and claims.
  - `User` class integrates with Flask-Login.
  - Hardcoded insurance plans for demo; easily extensible.

- **Forms & Validation**:
  - WTForms for all user input.
  - Custom validators (e.g., phone number uniqueness, agent district requirement).

- **Authentication**:
  - Role-based access control via decorators (`@farmer_required`, `@agent_required`).
  - Session management with Flask-Login.

---

## 5. Frontend Templates

- **Jinja2**: All pages are rendered with context-aware Jinja templates.
- **Bootstrap 5**: Consistent, responsive design across all devices.
- **Reusable Layout**: `base.html` provides a navbar, sidebar, and flash message system.
- **Dynamic Content**: Dashboards, plan lists, and forms adapt to user role and data.
- **JavaScript**: Used for form interactivity (e.g., show/hide fields, OTP input, dashboard widgets).

---

## 6. Noteworthy Implementation Details

- **Blueprint Modularity**: Each user role (farmer, agent) has its own blueprint and routes, making the codebase easy to extend.
- **In-Memory Data for Demo**: All user and insurance data is stored in Python dictionaries for simplicity—ideal for prototyping and hackathons.
- **Role-Based Decorators**: Custom decorators ensure only the right users access the right routes.
- **Form Validation**: Custom WTForms validators enforce business rules (e.g., agent must select a district).
- **Farmer Workflows**: Insurance and loan applications require document uploads, with geo-tagging and file type checks.
- **Agent Workflows**: Agents see only their assigned tasks, can verify claims, and submit reports with uploaded images.

---

## 7. Tech Stack (Detected)

- **Python 3.x**
- **Flask** (web framework)
- **Flask-Login** (authentication)
- **Flask-WTF** (forms & CSRF)
- **Bootstrap 5** (UI)
- **Jinja2** (templating)
- **requests** (API calls, e.g., weather)
- **Pillow** (image handling, if needed)
- **gunicorn** (production server)
- *(No SQLAlchemy in current code; all data is in-memory for demo)*
- **Front-end**: HTML5, CSS3, JavaScript, Font Awesome

*See `requirements.txt` for exact package list.*

---

## 8. Project-Based Learning

- **Blueprints**: Organize Flask apps by user role or feature for maintainability.
- **Forms**: Use Flask-WTF for secure, validated forms—custom validators make business logic explicit.
- **Role-Based Access**: Decorators are a clean way to enforce permissions.
- **Prototyping**: In-memory data stores are great for hackathons and MVPs; swap for a real DB for production.
- **UI/UX**: Bootstrap + Jinja2 enables rapid development of clean, responsive interfaces.

---

## 9. Getting Started (Local)

1. **Clone the repository**  
   ```powershell
   git clone <repo-url>
   cd AgriSure
   ```

2. **Create a virtual environment**  
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

3. **Install dependencies**  
   ```powershell
   pip install -r requirements.txt
   ```

4. **Run the application**  
   ```powershell
   python app.py
   ```

5. **Open in your browser**  
   Visit [http://localhost:5000](http://localhost:5000)

*No database setup required for demo mode. All data is in-memory and resets on restart.*

---

**AgriSure** is a living project—read the code, try it out, and contribute your ideas to help farmers thrive!
