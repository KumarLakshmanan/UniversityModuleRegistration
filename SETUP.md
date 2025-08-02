## 📁 Project Structure

```
module_registration_3/
├── course_registration/         # Main project directory (settings, URLs, WSGI)
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── accounts/                    # User accounts app (registration, login, email verification)
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── urls.py
│   ├── views.py
│   └── migrations/
├── students/                    # Student management app
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── urls.py
│   ├── views.py
│   └── migrations/
├── modules/                     # Module management app
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── urls.py
│   ├── views.py
│   ├── management/
│   └── migrations/
├── registrations/               # Module registration app
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── urls.py
│   ├── views.py
│   └── migrations/
├── api/                         # REST API app
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── urls.py
│   ├── views.py
│   └── migrations/
├── sitecore/                    # Core site app (home, about, contact)
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── urls.py
│   ├── views.py
│   ├── management/
│   └── migrations/
├── templates/                   # HTML templates
│   ├── base.html
│   ├── accounts/
│   ├── api/
│   ├── modules/
│   ├── registrations/
│   ├── sitecore/
│   └── students/
├── static/                      # Static files (CSS, JS)
│   ├── css/
│   └── js/
├── media/                       # Uploaded media files
│   └── student_photos/
├── manage.py                    # Django management script
├── requirements.txt             # Python dependencies
├── .gitignore
├── README.md
├── SETUP.md
└── module_registration_v3.sql   # Database schema
```

## 🚀 Running the Application

### Prerequisites
- Python 3.11+
- Virtual environment activated

### Setup Commands
```bash
# Navigate to project directory
cd d:\django\module_registration_3

# Create virtual environment
python3.11 -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Run migrations
python3.11 manage.py migrate

# Create superuser (if needed)
python3.11 manage.py createsuperuser

# Populate sample data
python3.11 manage.py seeddata

# Start development server
python3.11 manage.py runserver
```

### Access Points
- **Main Application**: http://127.0.0.1:8000/
- **Admin Interface**: http://127.0.0.1:8000/admin/
- **API Root**: http://127.0.0.1:8000/api/
- **API Token**: http://127.0.0.1:8000/api/auth/token/

## 📊 Sample Data

### Sample Students (Login Credentials)
- **Username**: `john_doe` | **Email**: `john.doe@student.edu` | **Password**: `student123`
- **Username**: `jane_smith` | **Email**: `jane.smith@student.edu` | **Password**: `student123`
- **Username**: `mike_johnson` | **Email**: `mike.johnson@student.edu` | **Password**: `student123`

### Sample Modules
- CS101 - Introduction to Computer Science (3 credits)
- WEB201 - Web Development Fundamentals (4 credits)
- DB301 - Database Systems (3 credits)
- ML401 - Machine Learning Basics (4 credits)
- MOB301 - Mobile App Development (4 credits)
- SE401 - Software Engineering Principles (3 credits)
- SEC301 - Cybersecurity Fundamentals (3 credits)
- DSA201 - Data Structures and Algorithms (4 credits)
- DMA201 - Digital Marketing Analytics (2 credits)
- PM301 - Project Management (2 credits)


## Database Configuration
For local development, use the following MySQL configuration:
```ini
[mysql]
user = root
password = 
database = module_registration_v1
host = localhost
```