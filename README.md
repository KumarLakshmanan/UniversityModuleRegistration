**Django Web Application Project – Developer Implementation Report**
**University Module Registration System | Cloud-Based | 2025**

## Objective

Develop a **monolithic Django web application** for managing student registration for university modules, including integration with Azure cloud services and demonstrating full compliance with functional, design, and deployment requirements.

## Page-by-Page Specification and Features

### 1. Home Page

**Purpose:** First impression landing page and gateway to the system
**Sections:**

* Hero Banner: Welcome message and Call-to-Action
* Our Services: Overview of module management, cloud reliability, and student experience
* Why Choose Us: System benefits (e.g., secure, user-friendly, cloud-hosted)
* Count-Up Stats: Dynamic counters for total modules, registered students, etc.
* Navigation Bar: Present on all pages with links to Home, Modules, About, Contact, Login, Register

**Features:**

* Responsive, consistently styled with base template inheritance

### 2. About Us Page

**Purpose:** Introduce the institution
**Sections:**

* University history and background
* Mission and vision
* Campus/learning highlights
* Internal anchor navigation for section jumping

**Features:**

* Structured, static content
* Collapsible panels or tabs optional

### 3. Contact Us Page

**Purpose:** Visitor communication
**Sections:**

* Contact Form: Name, Email, Subject, Message, Submit
* University Contact Details: address, email, phone
* Map Embed (optional)

**Features:**

* Form validation (client & server side)
* Success/failure user feedback messages

### 4. Modules Page

**Purpose:** List and manage all available modules
**Features:**

* List all modules with relevant details
* Search and pagination for modules by name/code
* Link to Module Detail page

### 5. Module Detail Page

**Purpose:** Show full details and registration options for a specific module
**Route:** `/modules/<code>/` (using code as slug)
**Features:**

* Show attributes: Name, Code, Credit, Category, Description, Availability
* List of all students registered to the module, with photo and registration date
* "Register" button (only visible if the student is eligible and module is open)
* "Unregister" button (only if already registered)
* Registration/unregistration performed via AJAX (no page reload)

### 6. Login Page

**Purpose:** Secure access for users
**Features:**

* Standard Django authentication (username, password)
* Clear error messages
* Redirect to dashboard on success; redirect unauthenticated users to home with warning

### 7. Registration (Sign-Up) Page

**Purpose:** Student registration
**Fields:** Username, Email, Password, Date of Birth, Address, City/Town, Country, Upload Photo

**Features:**

* On success: Create Django User + Student profile
* Auto-login or redirect to login page

### 8. Student Dashboard

**Purpose:** Central hub for student activities
**Features:**

* Profile summary (all info and profile photo)
* My Modules: list of modules registered for, with option to unregister (via AJAX)
* Quick Actions: update profile, view modules, logout, reset password

### 9. My Modules Page

**Purpose:** Show modules the student is registered in
**Features:**

* List each module with photo, registration date, and unregister option
* Pagination if many registrations

### 10. Profile View & Update Page

**Purpose:** View and edit student profile
**Features:**

* Pre-filled form with profile fields (editable as appropriate)
* Only the student can update their profile
* Upload profile image

### 11. AJAX Registration Handler

**Purpose:** Register/unregister modules without reloading
**Features:**

* All registration/unregistration actions done via AJAX
* JSON response with status
* Enforce one registration per student per module

### 12. Unauthorized Access Redirect Page

**Purpose:** Graceful warning and redirect for unauthorized access
**Features:**

* Redirect unauthenticated users trying to access restricted pages to home/login with an alert

### 13. Search and Pagination

**Purpose:** Manage large numbers of modules
**Features:**

* Search field for module name/code
* Pagination on modules list

### 14. Password Reset

**Purpose:** Secure password reset and recovery
**Features:**

* Django’s built-in password reset flow (email-based, with tokens)
* Request reset from login page

### 15. REST API Endpoints

**Purpose:** Provide RESTful integration and external data access
**Features:**

* Token-authenticated endpoints for listing/viewing modules, registrations, students
* At least one endpoint that fetches/displays content from a public external REST API
* Document endpoint URLs and usage instructions

### 16. OTP Email Verification and Password Reset

**Purpose:** Secure user validation using One-Time Password (OTP) sent via email using Google SMTP.

#### A. Email Verification After Registration

**Features:**

* Send a verification OTP to the registered email
* User must verify OTP before logging in
* OTP expires after a short duration (e.g., 10 minutes)
* Unverified users are denied access with a warning prompt

#### B. Forgot Password Using OTP

**Features:**

* User requests password reset via email
* System sends OTP to the registered email address using Gmail SMTP configuration
* OTP verification required before resetting password
* New password form displayed after successful OTP match

## Models Overview

**Built-in Models Used:**

* **User**: Standard Django auth model

### Custom Models

| Model                  | Key Fields/Relations                                           |
| ---------------------- | -------------------------------------------------------------- |
| Module                 | name, code (slug), credit, category, description, availability |
| Student                | OneToOne to User, dob, address, city, country, photo           |
| Registration           | student (FK), module (FK), date\_registered                    |
| UserProfile (optional) | Extra fields for User (phone, profile picture, bio, etc.)      |

## System Feature Checklist

*

## Email Delivery

**Technology Used:** Google SMTP (Gmail)

**Purpose:** To send OTPs securely for verification and password reset.

**Setup Notes:**

* Use Gmail's SMTP server (`smtp.gmail.com`, port 587)
* Enable 'App Passwords' in Google Account if 2FA is on
* Configure Django settings with email backend, host, port, and credentials

## Cloud Integration

* **Azure App Service** for hosting
* **Azure Database for MySQL** for production database
* **Azure Blob Storage** for all media/static content

## Suggested Navigation Map

| Page                  | URL Pattern        | Access         |
| --------------------- | ------------------ | -------------- |
| Home                  | `/`                | Public         |
| About Us              | `/about/`          | Public         |
| Contact Us            | `/contact/`        | Public         |
| Modules List          | `/modules/`        | Public/Student |
| Module Detail         | `/modules/<code>/` | Public/Student |
| Student Registration  | `/register/`       | Public         |
| Student Login         | `/login/`          | Public         |
| Dashboard/My Modules  | `/dashboard/`      | Authenticated  |
| Profile View/Edit     | `/profile/`        | Authenticated  |
| Password Reset        | `/password-reset/` | Public         |
| REST API              | `/api/`            | API Clients    |
| Unauthorized Redirect | `/unauthorized/`   | All            |

## Implementation Action Points

1. Remove all references to course/group models/views/UI.
2. Use only the Module, Student, and Registration models (plus optional UserProfile).
3. All module registration logic is based solely on students and modules.
4. Ensure one registration per student per module.
5. All page and view functionality as outlined above.
6. Complete REST API integration.
7. Use Django admin for staff CRUD operations on all models.
8. Consistent templates and navigation throughout.
9. Document Azure deployment, admin setup, and end-user guidance.



in the home page 4 sections needed.
and in about page 3 sections needed.

in the modules image is needed. 
use picsum for placeholder images.
like. https://picsum.photos/200/300

and remove all the description content. and replace it with the lorem ipsum text.

and also use all the images used in the home and about pages into picsum images.

and also change the design layout of the footer. and make it a new design layout. instead of traditional layout, use a more modern and sleek design.

and do not login admin in the
http://127.0.0.1:8000/auth/login/ page

and in the admin login please show all the details of form submits
http://127.0.0.1:8000/admin/
because now the contacts are not showing

and connect sql database with the below credentials
username -> 'root'
password -> ''
database -> 'module_registration_v1'
host -> 'localhost'

and migrate the database and seed initial data into mysql database.