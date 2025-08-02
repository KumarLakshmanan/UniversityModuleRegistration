## 📁 Project Structure

```
module_registration_2/
├── university_system/              # Main project directory (settings, URLs, WSGI, ASGI)
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   ├── asgi.py
│   └── db_backends/               # Custom DB backends (e.g., mysql)
├── accounts/                      # User accounts app (registration, login, OTP)
│   ├── admin.py
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── migrations/
├── students/                      # Student management app
│   ├── admin.py
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── migrations/
├── modules/                       # Module management app
│   ├── admin.py
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── management/commands/       # Custom management commands (e.g., seeddata)
│   └── migrations/
├── registrations/                 # Module registration app
│   ├── admin.py
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── migrations/
├── portalcontent/                 # Static portal content (home, about, contact)
│   ├── admin.py
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── management/commands/
│   └── migrations/
├── api/                           # REST API app
│   ├── admin.py
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── migrations/
├── templates/                     # HTML templates
│   ├── base.html
│   ├── accounts/
│   ├── emails/
│   ├── modules/
│   ├── portalcontent/
│   ├── registrations/
│   └── students/
├── static/                        # Static files (CSS, JS)
│   └── js/
├── media/                         # Uploaded media files
│   └── student_profiles/
├── manage.py                      # Django management script
├── requirements.txt               # Python dependencies
├── README.md
└── .gitignore
```

## 🚀 Running the Application

### Prerequisites
- Python 3.11+
- Virtual environment activated

### Setup Commands
```bash
# Navigate to project directory
cd d:\django\module_registration_2

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
- **Username**: `john_doe` | **Password**: `password123`
- **Username**: `jane_smith` | **Password**: `password123`
- **Username**: `bob_wilson` | **Password**: `password123`
- **Username**: `alice_brown` | **Password**: `password123`
- **Username**: `charlie_davis` | **Password**: `password123`

### Sample Modules (from seeddata.py)
- **CS101** - Introduction to Computer Science (3 credits, Core)
- **CS201** - Data Structures and Algorithms (4 credits, Core)
- **CS301** - Database Systems (3 credits, Specialized)
- **MATH101** - Calculus I (4 credits, Core)
- **MATH201** - Linear Algebra (3 credits, Core)
- **ENG101** - Academic Writing (3 credits, Core)
- **PHYS101** - Physics I (4 credits, Elective)
- **CS401** - Machine Learning (3 credits, Specialized)


## Database Configuration
For local development, use the following MySQL configuration:
```ini
[mysql]
user = root
password = 
database = module_registration_v1
host = localhost
```