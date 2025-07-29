from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Student
from modules.models import Module
from registrations.models import Registration
import json


class StudentsViewsTestCase(TestCase):
    """Test cases for students app views."""
    
    def setUp(self):
        """Set up test data."""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='TestPass123!',
            first_name='Test',
            last_name='User'
        )
        self.student = Student.objects.create(
            user=self.user,
            is_verified=True,
            phone='+1234567890',
            address='123 Test St'
        )
        
        # Create test modules
        self.module1 = Module.objects.create(
            code='CS101',
            name='Computer Science 101',
            description='Basic computer science course',
            credits=3,
            category='core',
            max_students=30
        )
        
        self.module2 = Module.objects.create(
            code='MATH101',
            name='Mathematics 101',
            description='Basic mathematics course',
            credits=4,
            category='core',
            max_students=25
        )
        
        # Create test registrations
        Registration.objects.create(
            student=self.student,
            module=self.module1,
            status='enrolled'
        )
    
    def test_dashboard_view_authenticated(self):
        """Test dashboard view for authenticated user."""
        self.client.login(username='testuser', password='TestPass123!')
        response = self.client.get(reverse('students:dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Dashboard')
        self.assertContains(response, 'Test User')
    
    def test_dashboard_view_unauthenticated(self):
        """Test dashboard view for unauthenticated user."""
        response = self.client.get(reverse('students:dashboard'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
    
    def test_profile_view_authenticated(self):
        """Test profile view for authenticated user."""
        self.client.login(username='testuser', password='TestPass123!')
        response = self.client.get(reverse('students:profile'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Profile')
        self.assertContains(response, self.student.user.username)
    
    def test_profile_view_unauthenticated(self):
        """Test profile view for unauthenticated user."""
        response = self.client.get(reverse('students:profile'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
    
    def test_profile_edit_view_get(self):
        """Test profile edit view GET request."""
        self.client.login(username='testuser', password='TestPass123!')
        response = self.client.get(reverse('students:profile_edit'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Edit Profile')
    
    def test_profile_edit_view_post_valid_data(self):
        """Test profile edit with valid data."""
        self.client.login(username='testuser', password='TestPass123!')
        
        data = {
            'first_name': 'Updated',
            'last_name': 'Name',
            'email': 'updated@example.com',
            'phone': '+9876543210',
            'address': '456 Updated St',
            'date_of_birth': '1995-01-01'
        }
        
        response = self.client.post(reverse('students:profile_edit'), data)
        self.assertEqual(response.status_code, 302)  # Redirect after success
        
        # Check updates were saved
        self.user.refresh_from_db()
        self.student.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Updated')
        self.assertEqual(self.user.email, 'updated@example.com')
        self.assertEqual(self.student.phone, '+9876543210')
        self.assertEqual(self.student.address, '456 Updated St')
    
    def test_profile_edit_view_post_invalid_data(self):
        """Test profile edit with invalid data."""
        self.client.login(username='testuser', password='TestPass123!')
        
        data = {
            'first_name': '',  # Required field
            'email': 'invalid-email'  # Invalid email
        }
        
        response = self.client.post(reverse('students:profile_edit'), data)
        self.assertEqual(response.status_code, 200)  # Stay on form with errors
        self.assertContains(response, 'This field is required')
    
    def test_profile_photo_upload(self):
        """Test profile photo upload."""
        self.client.login(username='testuser', password='TestPass123!')
        
        # Create a test image file
        image_content = b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x4c\x01\x00\x3b'
        image_file = SimpleUploadedFile(
            'test.gif',
            image_content,
            content_type='image/gif'
        )
        
        data = {
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test@example.com',
            'profile_picture': image_file
        }
        
        response = self.client.post(reverse('students:profile_edit'), data)
        self.assertEqual(response.status_code, 302)
        
        self.student.refresh_from_db()
        self.assertTrue(self.student.profile_picture)
    
    def test_dashboard_context_data(self):
        """Test dashboard view context data."""
        self.client.login(username='testuser', password='TestPass123!')
        response = self.client.get(reverse('students:dashboard'))
        
        context = response.context
        self.assertIn('student', context)
        self.assertIn('registered_modules', context)
        self.assertIn('total_credits', context)
        self.assertIn('recent_registrations', context)
        self.assertIn('available_modules', context)
        
        # Check values
        self.assertEqual(context['student'], self.student)
        self.assertEqual(context['total_credits'], 3)  # From CS101
        self.assertTrue(len(context['registered_modules']) >= 1)
    
    def test_student_model_string_representation(self):
        """Test Student model __str__ method."""
        expected = f"{self.student.user.username} - Test User"
        self.assertEqual(str(self.student), expected)
    
    def test_student_model_creation_with_defaults(self):
        """Test student model creation with default values."""
        new_user = User.objects.create_user(
            username='newuser',
            email='new@example.com',
            password='NewPass123!'
        )
        new_student = Student.objects.create(user=new_user)
        
        self.assertFalse(new_student.is_verified)
        self.assertEqual(new_student.user, new_user)
    
    def test_dashboard_stats_calculation(self):
        """Test dashboard statistics calculation."""
        # Add more registrations to test stats
        Registration.objects.create(
            student=self.student,
            module=self.module2,
            status='completed'
        )
        
        self.client.login(username='testuser', password='TestPass123!')
        response = self.client.get(reverse('students:dashboard'))
        
        context = response.context
        stats = context['stats']
        
        self.assertEqual(stats['enrolled'], 1)  # CS101
        self.assertEqual(stats['completed'], 1)  # MATH101
        self.assertEqual(stats['total'], 2)
    
    def test_profile_edit_duplicate_email(self):
        """Test profile edit with duplicate email."""
        # Create another user with email we'll try to use
        User.objects.create_user(
            username='otheruser',
            email='other@example.com',
            password='OtherPass123!'
        )
        
        self.client.login(username='testuser', password='TestPass123!')
        
        data = {
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'other@example.com',  # Duplicate email
            'phone': '+1234567890'
        }
        
        response = self.client.post(reverse('students:profile_edit'), data)
        self.assertEqual(response.status_code, 200)  # Stay on form
        self.assertContains(response, 'already exists')


class StudentModelTestCase(TestCase):
    """Test cases for Student model."""
    
    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='TestPass123!'
        )
    
    def test_student_creation(self):
        """Test student creation."""
        student = Student.objects.create(
            user=self.user,
            phone='+1234567890'
        )
        
        self.assertEqual(student.user, self.user)
        self.assertFalse(student.is_verified)  # Default value
        self.assertTrue(hasattr(student, 'created_at'))
    
    def test_student_uniqueness(self):
        """Test student user uniqueness."""
        student1 = Student.objects.create(user=self.user)
        
        user2 = User.objects.create_user(
            username='testuser2',
            email='test2@example.com',
            password='TestPass123!'
        )
        student2 = Student.objects.create(user=user2)
        
        self.assertNotEqual(student1.user, student2.user)
    
    def test_student_profile_picture_upload_path(self):
        """Test profile picture upload field."""
        student = Student.objects.create(user=self.user)
        
        # The upload path should be to student_photos folder
        field = student._meta.get_field('photo')
        self.assertEqual(field.upload_to, 'student_photos/')
        # We can't directly test the upload_to function easily,
        # but we can check the field configuration
        self.assertTrue(hasattr(student, 'profile_picture'))
    
    def test_student_verification_status(self):
        """Test student verification status."""
        student = Student.objects.create(
            user=self.user,
            is_verified=False
        )
        
        self.assertFalse(student.is_verified)
        
        # Verify student
        student.is_verified = True
        student.save()
        
        student.refresh_from_db()
        self.assertTrue(student.is_verified)
