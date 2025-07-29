from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.core import mail
from students.models import Student, OTP
from django.utils import timezone
from datetime import timedelta
import json


class AccountsViewsTestCase(TestCase):
    """Test cases for accounts app views."""
    
    def setUp(self):
        """Set up test data."""
        self.client = Client()
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'TestPass123!',
            'password_confirm': 'TestPass123!',
            'first_name': 'Test',
            'last_name': 'User'
        }
    
    def test_login_view_get(self):
        """Test login view GET request."""
        response = self.client.get(reverse('accounts:login'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Login')
    
    def test_login_valid_user(self):
        """Test login with valid credentials."""
        # Create verified user
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='TestPass123!'
        )
        student = Student.objects.create(user=user, is_verified=True)
        
        response = self.client.post(reverse('accounts:login'), {
            'username': 'testuser',
            'password': 'TestPass123!'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after login
        self.assertTrue(response.wsgi_request.user.is_authenticated)
    
    def test_login_unverified_user(self):
        """Test login with unverified user."""
        # Create unverified user
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='TestPass123!'
        )
        student = Student.objects.create(user=user, is_verified=False)
        
        response = self.client.post(reverse('accounts:login'), {
            'username': 'testuser',
            'password': 'TestPass123!'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Please verify your email')
    
    def test_login_invalid_credentials(self):
        """Test login with invalid credentials."""
        response = self.client.post(reverse('accounts:login'), {
            'username': 'invalid',
            'password': 'invalid'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Invalid username or password')
    
    def test_register_view_get(self):
        """Test register view GET request."""
        response = self.client.get(reverse('accounts:register'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Register')
    
    def test_register_valid_data(self):
        """Test registration with valid data."""
        response = self.client.post(reverse('accounts:register'), self.user_data)
        self.assertEqual(response.status_code, 302)  # Redirect to verify email
        
        # Check user was created
        self.assertTrue(User.objects.filter(username='testuser').exists())
        user = User.objects.get(username='testuser')
        self.assertTrue(hasattr(user, 'student_profile'))
        self.assertFalse(user.student_profile.is_verified)
        
        # Check OTP was created
        self.assertTrue(OTP.objects.filter(user=user, purpose='verification').exists())
    
    def test_register_password_mismatch(self):
        """Test registration with password mismatch."""
        data = self.user_data.copy()
        data['password_confirm'] = 'DifferentPassword'
        
        response = self.client.post(reverse('accounts:register'), data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Passwords do not match')
        self.assertFalse(User.objects.filter(username='testuser').exists())
    
    def test_register_duplicate_username(self):
        """Test registration with existing username."""
        User.objects.create_user(username='testuser', email='other@example.com')
        
        response = self.client.post(reverse('accounts:register'), self.user_data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Username already exists')
    
    def test_register_duplicate_email(self):
        """Test registration with existing email."""
        User.objects.create_user(username='otheruser', email='test@example.com')
        
        response = self.client.post(reverse('accounts:register'), self.user_data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Email already exists')
    
    def test_verify_email_view_get(self):
        """Test verify email view GET request."""
        response = self.client.get(reverse('accounts:verify_email'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Verify Your Email')
    
    def test_verify_email_valid_otp(self):
        """Test email verification with valid OTP."""
        # Create user and OTP
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='TestPass123!'
        )
        student = Student.objects.create(user=user, is_verified=False)
        otp = OTP.objects.create(
            user=user,
            otp_code='123456',
            purpose='verification',
            expires_at=timezone.now() + timedelta(minutes=10)
        )
        
        response = self.client.post(reverse('accounts:verify_email'), {
            'email': 'test@example.com',
            'otp_code': '123456'
        })
        self.assertEqual(response.status_code, 302)  # Redirect to login
        
        # Check user is verified
        student.refresh_from_db()
        self.assertTrue(student.is_verified)
        
        # Check OTP is marked as used
        otp.refresh_from_db()
        self.assertTrue(otp.is_used)
    
    def test_verify_email_invalid_otp(self):
        """Test email verification with invalid OTP."""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='TestPass123!'
        )
        student = Student.objects.create(user=user, is_verified=False)
        
        response = self.client.post(reverse('accounts:verify_email'), {
            'email': 'test@example.com',
            'otp_code': '999999'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Invalid or expired OTP')
        
        # Check user is still not verified
        student.refresh_from_db()
        self.assertFalse(student.is_verified)
    
    def test_verify_email_expired_otp(self):
        """Test email verification with expired OTP."""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='TestPass123!'
        )
        student = Student.objects.create(user=user, is_verified=False)
        otp = OTP.objects.create(
            user=user,
            otp_code='123456',
            purpose='verification',
            expires_at=timezone.now() - timedelta(minutes=1)  # Expired
        )
        
        response = self.client.post(reverse('accounts:verify_email'), {
            'email': 'test@example.com',
            'otp_code': '123456'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Invalid or expired OTP')
    
    def test_logout_view(self):
        """Test logout functionality."""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='TestPass123!'
        )
        self.client.login(username='testuser', password='TestPass123!')
        
        response = self.client.get(reverse('accounts:logout'))
        self.assertEqual(response.status_code, 302)  # Redirect to home
    
    def test_password_reset_request_valid_email(self):
        """Test password reset request with valid email."""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='TestPass123!'
        )
        
        response = self.client.post(reverse('accounts:password_reset'), {
            'email': 'test@example.com'
        })
        self.assertEqual(response.status_code, 302)
        
        # Check OTP was created
        self.assertTrue(OTP.objects.filter(
            user=user, purpose='password_reset'
        ).exists())
    
    def test_password_reset_request_invalid_email(self):
        """Test password reset request with invalid email."""
        response = self.client.post(reverse('accounts:password_reset'), {
            'email': 'nonexistent@example.com'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'User with this email does not exist')
    
    def test_password_reset_confirm_valid_otp(self):
        """Test password reset confirmation with valid OTP."""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='OldPass123!'
        )
        otp = OTP.objects.create(
            user=user,
            otp_code='123456',
            purpose='password_reset',
            expires_at=timezone.now() + timedelta(minutes=10)
        )
        
        response = self.client.post(reverse('accounts:password_reset_confirm'), {
            'email': 'test@example.com',
            'otp_code': '123456',
            'new_password': 'NewPass123!',
            'password_confirm': 'NewPass123!'
        })
        self.assertEqual(response.status_code, 302)
        
        # Check password was changed
        user.refresh_from_db()
        self.assertTrue(user.check_password('NewPass123!'))
        
        # Check OTP is marked as used
        otp.refresh_from_db()
        self.assertTrue(otp.is_used)
    
    def test_password_reset_confirm_password_mismatch(self):
        """Test password reset confirmation with password mismatch."""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='OldPass123!'
        )
        OTP.objects.create(
            user=user,
            otp_code='123456',
            purpose='password_reset',
            expires_at=timezone.now() + timedelta(minutes=10)
        )
        
        response = self.client.post(reverse('accounts:password_reset_confirm'), {
            'email': 'test@example.com',
            'otp_code': '123456',
            'new_password': 'NewPass123!',
            'password_confirm': 'DifferentPass123!'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Passwords do not match')


class OTPModelTestCase(TestCase):
    """Test cases for OTP model."""
    
    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='TestPass123!'
        )
    
    def test_otp_is_valid_property(self):
        """Test OTP is_valid property."""
        # Valid OTP
        otp = OTP.objects.create(
            user=self.user,
            otp_code='123456',
            purpose='verification',
            expires_at=timezone.now() + timedelta(minutes=10)
        )
        self.assertTrue(otp.is_valid)
        
        # Expired OTP
        expired_otp = OTP.objects.create(
            user=self.user,
            otp_code='654321',
            purpose='verification',
            expires_at=timezone.now() - timedelta(minutes=1)
        )
        self.assertFalse(expired_otp.is_valid)
        
        # Used OTP
        used_otp = OTP.objects.create(
            user=self.user,
            otp_code='111111',
            purpose='verification',
            expires_at=timezone.now() + timedelta(minutes=10),
            is_used=True
        )
        self.assertFalse(used_otp.is_valid)
