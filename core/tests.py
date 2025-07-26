from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from students.models import Student
from modules.models import Module, Registration


class BasicViewsTestCase(TestCase):
    """Basic test cases for core functionality"""
    
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
        self.module = Module.objects.create(
            name='Test Module',
            code='TEST101',
            credit=3,
            description='Test module description',
            max_students=50
        )
    
    def test_home_page_loads(self):
        """Test home page loads successfully"""
        response = self.client.get(reverse('core:home'))
        self.assertEqual(response.status_code, 200)
    
    def test_modules_list_loads(self):
        """Test modules list page loads successfully"""
        response = self.client.get(reverse('modules:list'))
        self.assertEqual(response.status_code, 200)
    
    def test_module_detail_loads(self):
        """Test module detail page loads successfully"""
        response = self.client.get(reverse('modules:detail', kwargs={'code': self.module.code}))
        self.assertEqual(response.status_code, 200)
    
    def test_student_dashboard_requires_login(self):
        """Test dashboard requires login"""
        response = self.client.get(reverse('students:dashboard'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
    
    def test_student_dashboard_works_when_logged_in(self):
        """Test dashboard works for authenticated user"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('students:dashboard'))
        self.assertEqual(response.status_code, 200)
    
    def test_student_profile_works_when_logged_in(self):
        """Test profile works for authenticated user"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('students:profile'))
        self.assertEqual(response.status_code, 200)
    
    def test_unique_registration_constraint(self):
        """Test that a student can only register once per module"""
        # Create first registration
        Registration.objects.create(student=self.student, module=self.module)
        
        # Try to create duplicate registration
        with self.assertRaises(Exception):
            Registration.objects.create(student=self.student, module=self.module)
