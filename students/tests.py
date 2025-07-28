from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from students.models import Student, EmailVerification, PasswordResetOTP
from modules.models import Module, Registration


class StudentViewsTestCase(TestCase):
    """Test cases for student views"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.student = Student.objects.create(
            user=self.user,
            date_of_birth='1990-01-01',
            address='123 Test St',
            city='Test City',
            country='Test Country'
        )

    def test_login_page_loads(self):
        """Test login page loads successfully"""
        response = self.client.get(reverse('students:login'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Student Login')

    def test_register_page_loads(self):
        """Test register page loads successfully"""
        response = self.client.get(reverse('students:register'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Student Registration')

    def test_login_functionality(self):
        """Test login functionality"""
        response = self.client.post(reverse('students:login'), {
            'username': 'testuser',
            'password': 'testpass123'
        })
        # Should redirect to dashboard after successful login
        self.assertEqual(response.status_code, 302)

    def test_dashboard_requires_login(self):
        """Test dashboard requires login"""
        response = self.client.get(reverse('students:dashboard'))
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_dashboard_authenticated(self):
        """Test dashboard loads for authenticated user"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('students:dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Dashboard')

    def test_profile_authenticated(self):
        """Test profile loads for authenticated user"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('students:profile'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'My Profile')

    def test_profile_edit_get(self):
        """Test profile edit page loads"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('students:profile_edit'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Edit Profile')

    def test_profile_edit_post(self):
        """Test profile edit form submission"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('students:profile_edit'), {
            'first_name': 'Updated',
            'last_name': 'Name',
            'email': 'updated@example.com',
            'date_of_birth': '1995-01-01',
            'address': 'Updated Address',
            'city': 'Updated City',
            'country': 'Updated Country'
        })
        # Should redirect to profile after successful update
        self.assertEqual(response.status_code, 302)

        # Verify update
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Updated')

    def test_logout_redirect(self):
        """Test logout redirects properly"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(
            reverse('students:logout'))  # POST instead of GET
        self.assertEqual(response.status_code, 302)  # Redirect after logout

    def test_student_registration_form(self):
        """Test student registration form submission"""
        response = self.client.post(reverse('students:register'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'first_name': 'New',
            'last_name': 'User',
            'password1': 'newpass123',
            'password2': 'newpass123',
            'date_of_birth': '1995-01-01',
            'address': '456 New St',
            'city': 'New City',
            'country': 'New Country'
        })
        # Should redirect or show success message
        self.assertIn(response.status_code, [200, 302])

    def test_student_model_creation(self):
        """Test student model creation"""
        new_user = User.objects.create_user(
            username='newuser2',
            email='newuser2@example.com',
            password='pass123'
        )
        new_student = Student.objects.create(
            user=new_user,
            date_of_birth='1992-01-01',
            address='789 Another St',
            city='Another City',
            country='Another Country'
        )
        self.assertEqual(new_student.user.username, 'newuser2')
        self.assertFalse(new_student.is_email_verified)
