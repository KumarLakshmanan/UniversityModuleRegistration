# Course Module Registration System  
**Django Monolithic Web Application | Materialize CSS Frontend | SQLite DB (initially)**

## 1. Stack & Configuration

- **Backend:** Django (latest stable) monolithic project with Django REST Framework for API design.
- **Frontend:** Django templates with [Materialize CSS](https://materializecss.com/) for modern, responsive UI styling.
- **Database:** SQLite 3 for development and testing phase; planned upgrade to MySQL in production.
- **Email:** Google SMTP (Gmail) used for all OTP email delivery.
- **Authentication:** Django’s built-in User model leveraged; OTP-based verification integrated for sign-up and password reset.
- **Static & Media Files:** Local filesystem in dev, switch to cloud storage (e.g. Azure Blob Storage) planned later.
- **Testing:** Django `TestCase` and REST Framework’s `APIClient` for API testing.

## 2. Apps & Primary Responsibilities

| App Name       | Responsibilities                                                      |
|----------------|----------------------------------------------------------------------|
| `accounts`     | User registration (signup), login/logout, OTP handling, password reset |
| `students`     | Student profile CRUD, dashboard data, profile updates                  |
| `modules`      | Module catalog management, module search, detail retrieval             |
| `registrations`| Student-module enrollment/unregistration tracking                       |
| `sitecore`     | Static and marketing pages: Home, About, Contact, FAQs                |
| `api`          | Centralized REST API routing and viewsets for all app models          |

## 3. Database Setup, Migrations, and Seed Data

- **Database Configuration (settings.py):**

  ```python
  DATABASES = {
      'default': {
          'ENGINE': 'django.db.backends.sqlite3',
          'NAME': BASE_DIR / 'db.sqlite3',
      }
  }
  ```

- **Migrations:**

  Run the following commands whenever models are created/modified:
  ```bash
  python manage.py makemigrations
  python manage.py migrate
  ```

- **Seed Data:**

  - Prepare management commands (e.g., `seeddata`) in respective apps to populate initial data such as:
    - Sample Modules (5–10 entries)
    - Sample Students (5 with profiles linked to User objects)
    - Sample Registrations tying students to modules
  - Alternatively, use fixture files (`JSON` or `YAML`) to load data via:
    ```bash
    python manage.py loaddata 
    ```

- **User Accounts for Testing:**
  - Create both verified and unverified students.
  - Include a superuser for Django admin access.

## 4. App Test Plan: `tests.py` Content Outline

Each app contains a `tests.py` with test classes that validate the API endpoints, views, and business logic relevant to that app.

### A. `accounts/tests.py`

- **Tests:**
  - Registration with valid/invalid data.
  - Email Verification OTP: valid, expired, invalid OTP.
  - Login success/failure, including unverified user rejection.
  - Password Reset flows:
    - Request OTP
    - Verify OTP
    - Reset password
  - Email sending mocked and verified.
  - Access protection for unverified users.

### B. `students/tests.py`

- **Tests:**
  - Profile GET and update with valid and invalid data.
  - Photo upload and validation.
  - Dashboard data retrieval.
  - Permissions test: unauthenticated users denied access.

### C. `modules/tests.py`

- **Tests:**
  - List and retrieve modules (search, pagination).
  - Module detail responses with enrolled students included.
  - Admin-only create, update, and delete access via Django admin (optional API test).
  - Public access enforcement.

### D. `registrations/tests.py`

- **Tests:**
  - Module registration for a student (success, duplicate registration prevention).
  - Unregistration by authorized student only.
  - AJAX response JSON correctness.
  - Edge cases: registering closed/unavailable modules.

### E. `sitecore/tests.py`

- **Tests:**
  - Load Home, About, Contact pages.
  - Submit Contact form valid and invalid data.
  - Verify email sent on Contact form (mocked).
  - Static content integrity.

### F. `api/tests.py` (if separate app)

- **Tests:**
  - Authentication and token management.
  - Permission enforcement across endpoints.
  - External API data fetching (mocked).
  - System stats endpoint correctness.

## 5. Page-by-Page Components & Functionalities

| Page Name         | URL Pattern           | Components                                           | Functionality Summary                                                   |
|-------------------|-----------------------|----------------------------------------------------|------------------------------------------------------------------------|
| Home              | `/`                   | Hero banner, services overview, stats counters, nav bar | Display system stats; marketing content; navigation                    |
| About             | `/about/`             | Institution history, mission, campus highlights    | Static informative content with optional collapsibles                 |
| Contact           | `/contact/`           | Contact form, contact details, optional map        | Form submits via AJAX; validation and feedback                        |
| Modules List      | `/modules/`           | Search bar, paginated list of modules               | Search/filter by code/name; link to module detail                      |
| Module Detail     | `/modules//`    | Module info, students list, registration buttons    | Register/unregister via AJAX; dynamic button visibility                |
| Register          | `/register/`          | Registration form (username, email, password, etc.)| Form submission creates user/student profiles; sends verification OTP  |
| Login             | `/login/`             | Username/password fields, login button               | Authenticates user; error messages; redirection on success            |
| Dashboard         | `/dashboard/`         | Profile summary, registered module list, quick links| Central student hub; data from profile and registration APIs          |
| My Modules        | `/my-modules/`        | List of student-registered modules, unregister btn  | Paginated with AJAX unregister action                                 |
| Profile           | `/profile/`           | Pre-filled editable profile form, photo upload      | View and update student profile fields                                 |
| Password Reset    | `/password-reset/`    | Email input, OTP verification, set new password     | Multi-step OTP-based reset via API calls                              |
| Unauthorized      | `/unauthorized/`      | Warning message, redirect links                      | Graceful redirect handling unauthorized users                         |
| REST API          | `/api/`               | API root, Endpoint documentation, token auth        | Provides all dynamic data and actions via REST                        |

## 6. Implementation Note

- **API-Driven UI**: All dynamic page content and actions happen via REST API calls; the UI uses AJAX or similar. Django views serve templates only.
- **Materialize CSS**: Used throughout for consistent and responsive UI styling. Setup via materialize css.
- **Email OTP Flow**: OTPs must expire after 10 minutes and enforce single-use.
- **Testing**: Use Django built-in test client and REST framework’s `APIClient`. Mocks for email sending.
- **Security**: Unverified users cannot access restricted APIs or pages; all API endpoints enforce permission checks.
- **Code Comments and Docs**: Professional style, no mention or hints of AI-generated content.
- **Future Proofing**: SQLite replaced by MySQL in production with minimal configuration changes.

## CUSTOM MODELS

| Model           | Key Fields/Relations                                                  |
|-----------------|----------------------------------------------------------------------|
| **Module**      | name, code (slug), credit, category, description, availability status |
| **Student**     | OneToOne to User; fields: dob, address, city, country, photo          |
| **Registration**| FK to Student, FK to Module, date_registered                          |
| **UserProfile** (optional) | OneToOne to User; phone, profile_picture, bio, additional attrs |

- Use Django’s built-in User model.
- UserProfile for optional fields beyond the Student model.

## NAVIGATION MAP

| Page / Function            | URL Pattern            | Access Level       | Description                          |
|---------------------------|------------------------|--------------------|------------------------------------|
| Home                      | `/`                    | Public             | Landing page with system stats     |
| About                     | `/about/`              | Public             | About the institution              |
| Contact                   | `/contact/`            | Public             | Contact form                      |
| Modules List              | `/modules/`            | Public             | Browse/search modules              |
| Module Detail             | `/modules//`     | Public/Student      | Module info, registration          |
| Registration (Sign-Up)    | `/register/`           | Public             | New student creation + OTP OTP     |
| Login                     | `/login/`              | Public             | Existing user login                |
| Dashboard                 | `/dashboard/`          | Authenticated User | Student’s personal hub            |
| My Modules                | `/my-modules/`         | Authenticated User | Registered modules list            |
| Profile                   | `/profile/`            | Authenticated User | View and update profile            |
| Password Reset            | `/password-reset/`     | Public             | Request/reset password via OTP     |
| Unauthorized              | `/unauthorized/`       | All                | Unauthorized access warning        |
| REST API root             | `/api/`                | Auth/API Clients   | Root path for API endpoints        |

**Navigation Bar**

- Present on every page.
- Displays links based on authentication status:
  - For guests: Home, Modules, About, Contact, Login, Register
  - For authenticated students: Home, Modules, My Modules, Dashboard, Profile, Logout

If you require additional details such as API response formats, sample templates for each page, or seed data scripts, please let me know!