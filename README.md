# University Module Registration System (Local/SQLite Phase)

## 1. Stack & Configuration

- **Backend:** Django monolith (using Django REST Framework for all business/API logic)
- **Frontend:** Django templates using [Tailwind CSS](https://django-tailwind.readthedocs.io/);
  all pages dynamically fetch (AJAX) from API endpoints.
- **Database:** Local `sqlite3` file for development and testing.  
  (_Updatable to MySQL in the next phase via settings/migrations._)
- **Email:** Gmail SMTP for OTP and notifications.

## 2. Apps & Primary Responsibilities

| App Name      | Responsibilities                                        |
|---------------|---------------------------------------------------------|
| `accounts`    | User registration, login, OTP flows, password management|
| `students`    | Student profile management, dashboard                  |
| `modules`     | Module listing, search, detail, registration logic     |
| `registrations`| Track/manage student-module enrolment                  |
| `sitecore`    | Home, About, Contact, static informational pages        |
| `api`         | DRF-based viewsets for all core models (API interface) |

## 3. Database Setup, Migrations, and Seed Data

**Database:**  
Development uses SQLite (`db.sqlite3`). Settings in `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

**Migrations:**  
- Run `python manage.py makemigrations` for each app after model creation.
- Initialize with `python manage.py migrate`.

**Seed Data:**  
- Create a Django `management/commands/seeddata.py` script in each app for initial fixtures:
    - Example: Create 5 modules, 5 fake students, and several student-module registrations.
    - Users for testing: one staff, two students (one OTP-verified, one not).

**Fixtures:**  
- Alternatively, place JSON/YAML fixtures under each app’s `fixtures/` and load with `loaddata`.

## 4. App Test Plan: `tests.py` content outline

**Each app contains its own `tests.py` that:**
- Validates all API endpoints (CRUD, authentication, registration, etc).
- Checks permissions/auth where required.
- Ensures all USER and staff flows.
- Verifies core business rules (e.g., one registration per student per module).

### **A. `accounts/tests.py`**

- **User registration** (POST `/api/register/`)
    - Creates user, triggers OTP email, user inactive until OTP confirmed.
    - Fail if required data missing, invalid email, etc.
- **OTP verification** (POST `/api/verify-register-otp/`)
    - Only activates on correct OTP, not after expiry or reuse.
- **Login** (POST `/api/login/`)
    - Success for valid credentials, fail for bad/unverified.
- **Password reset** (OTP request, OTP verify, password change).
    - Only allows password change after correct OTP.
- **Security:** Prevent access to student APIs if unverified.
- **Email sending** checked via test backend.

### **B. `students/tests.py`**

- **Profile fetch, update** (`/api/profile/` GET/PUT)
    - Only accessible by logged-in/verified student.
    - Photo upload support.
- **Dashboard data** (profile + "My Modules" summary).
- **Permissions:** Access blocked if unauthenticated.

### **C. `modules/tests.py`**

- **List/Search Modules** (`/api/modules/`)
    - Search by name/code, pagination.
- **Module Detail** (`/api/modules//`)
    - Provides module info plus student list.
- **Add/Update/Delete**: Restricted to staff/admin via Django admin.
- **Public access:** Module list/details viewable to all.

### **D. `registrations/tests.py`**

- **Register for module** (`/api/modules//register/`)
    - Only allowed if slot available, not already registered.
- **Unregister** (`/api/modules//unregister/`)
    - Only by that student.
- **API Response:** Returns correct JSON status (success/fail).

### **E. `sitecore/tests.py`**

- **Home, About, Contact** page loads.
- **Contact form API** (`/api/contact/`)
    - Form validation and backend message handling.
    - Email actually sent.

### **F. `api/tests.py`** (if a separate app; else covered by above)

- **Token/session authentication for all API endpoints.**
- **Permission checks** on all routes (unauthenticated/unauthorized denied).
- **External API fetching** endpoint returns live or mocked third-party data.
- **Stats** endpoint returns accurate system metrics.

## 5. Page-by-Page Components & Functionalities

### **1. Home Page `/`**
- **Components:**
    - Hero banner (welcome, CTA)
    - Services summary cards
    - "Why Choose Us" feature list
    - Animated stat counters (students/modules/registrations; fetched by `/api/stats/`)
    - Tailwind-styled navigation bar
- **Functionality:**  
    Rendered server-side, dynamic stats fetched via JS and updated live.

### **2. About Us `/about/`**
- **Components:**
    - Timeline/description for history
    - Mission & vision
    - Campus highlights (images/icons)
    - In-page navigation (anchors or collapsibles)
- **Functionality:**  
    Static page, may fetch about text/sections from `/api/about/` if desired.

### **3. Contact Us `/contact/`**
- **Components:**
    - Contact form (name, email, subject, message)
    - Validation (client & server)
    - Feedback alerts (success/failure)
    - University address/email/phone info card
    - (Optional) Map embed
- **Functionality:**  
    Sends AJAX POST to `/api/contact/`. Shows result without reload.

### **4. Modules List `/modules/`**
- **Components:**
    - Search field (live filter)
    - Paginated module grid/list
    - Each item: name, code, category, credit, open/closed badge, view/details link
- **Functionality:**
    Fetches and displays via `/api/modules/`; supports query params.

### **5. Module Detail `/modules//`**
- **Components:**
    - Full module info (title, code, desc, etc), availability status
    - Table/list of students (name, photo, reg. date)
    - Register/Unregister button (stateful, via JS)
- **Functionality:**  
    - Buttons do AJAX POST to `/api/modules//register/` or `/unregister/`
    - UI updates dynamically on success/error

### **6. Register/Login/OTP Pages `/register/`, `/login/`, `/otp/`**
- **Components:**
    - Multi-section card for login or signup
    - Registration form inputs, photo upload
    - OTP validation modal/form after sign-up
    - Error/success feedback
- **Functionality:**  
    Forms POST via AJAX to APIs; OTP required for user activation; allows resend OTP.

### **7. Dashboard `/dashboard/`**
- **Components:**
    - Profile summary card (all fields + photo)
    - “My Modules” mini-list with unregister links
    - Quick action buttons (update profile, logout, reset password)
- **Functionality:**
    All data fetched from `/api/profile/` and `/api/my-modules/`.

### **8. My Modules `/my-modules/`**
- **Components:**
    - Paginated/scrollable personal modules list with details, registration date, unregister button
- **Functionality:**  
    Fetches via `/api/my-modules/`; unregister is AJAX.

### **9. Profile `/profile/`**
- **Components:**
    - Form with all fields (pre-filled)
    - Profile photo (upload/change)
    - Save/cancel controls
- **Functionality:**  
    Fetch/update via `/api/profile/` GET/PUT.

### **10. Password Reset `/password-reset/`**
- **Components:**
    - Request form: email input
    - OTP input modal/section
    - New password set after OTP
    - Step-by-step feedback
- **Functionality:**  
    All flows via API; cannot reset without verified OTP.

### **11. Unauthorized `/unauthorized/`**
- **Components:**
    - Warning alert
    - Login/home/redirect links/timeouts
- **Functionality:**  
    Shown for 401/403 errors

## 6. Implementation Note

- **No code/content should indicate AI authorship or provenance in code comments, docs, or UI**
- All comments and documentation should be in a professional, project-focused tone.


## CUSTOM MODELS

| Model           | Key Fields/Relations                                                      |
|-----------------|--------------------------------------------------------------------------|
| **Module**      | name (Char), code (Slug), credit (Int), category (Char), description (Text), availability (Bool/Enum)  |
| **Student**     | OneToOne to User, dob (Date), address (Char), city (Char), country (Char), photo (Image)          |
| **Registration**| student (ForeignKey), module (ForeignKey), date_registered (DateTime)                     |
| **UserProfile** (optional) | OneToOneField to User, phone (Char), profile_picture (Image), bio (Text), etc.    |

- Use Django’s built-in **User** model for authentication.
- If you need to add extra user data, create the `UserProfile` model linked with a `OneToOneField` to `User` (for optional fields like phone, bio, etc).

## NAVIGATION MAP

A clear **navigation map** should be included in both documentation and for future frontend implementation. Below is the primary URL structure and the minimum access levels required for each route:

| Page/Function               | URL Pattern                 | Access            | Description                         |
|-----------------------------|-----------------------------|-------------------|-------------------------------------|
| **Home**                    | `/`                         | Public            | Landing/home page                   |
| **About Us**                | `/about/`                   | Public            | About the institution               |
| **Contact Us**              | `/contact/`                 | Public            | Contact form + details              |
| **Modules List**            | `/modules/`                 | Public, Student   | List/search all modules             |
| **Module Detail**           | `/modules//`          | Public, Student   | Module details, registration        |
| **Register (Sign-Up)**      | `/register/`                | Public            | Create student user                 |
| **Login**                   | `/login/`                   | Public            | Login existing student              |
| **OTP Verification**        | `/otp/`                     | Public (new users)| Email OTP verification after signup |
| **Dashboard**               | `/dashboard/`               | Authenticated     | Student hub/profile                 |
| **My Modules**              | `/my-modules/`              | Authenticated     | Modules registered by student       |
| **Profile (View/Edit)**     | `/profile/`                 | Authenticated     | Student profile management          |
| **Password Reset**          | `/password-reset/`          | Public            | Initiate/reset password (OTP)       |
| **REST API**                | `/api/`                     | Auth/Token clients| All backend API endpoints           |
| **Unauthorized**            | `/unauthorized/`            | All               | Shown for forbidden access          |

### Navigation Bar
- Every page includes a top navigation bar with at least: Home, Modules, About, Contact, Login/Register or Dashboard (if logged in).

**Summary:**
- The navigation map makes site structure simple for both end-users and developers.
- Custom models encompass every user, module, registration, and (optionally) extended profile field you may need.
