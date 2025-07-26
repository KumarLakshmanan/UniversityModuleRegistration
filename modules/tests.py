from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from students.models import Student
from modules.models import Module, Registration


class ModuleViewsTestCase(TestCase):
    """Test cases for module views"""
    
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
    
    def test_module_list_loads(self):
        """Test modules list page loads successfully"""
        response = self.client.get(reverse('modules:list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Available Modules')
    
    def test_module_detail_loads(self):
        """Test module detail page loads successfully"""
        response = self.client.get(reverse('modules:detail', kwargs={'code': self.module.code}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.module.name)
    
    def test_module_registration_requires_login(self):
        """Test module registration requires login"""
        response = self.client.post(reverse('modules:register', kwargs={'code': self.module.code}))
        self.assertEqual(response.status_code, 302)  # Redirect to login
    
    def test_module_registration_authenticated(self):
        """Test module registration for authenticated user"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('modules:register', kwargs={'code': self.module.code}))
        # Should redirect or return JSON response
        self.assertIn(response.status_code, [200, 302])
    
    def test_module_model_properties(self):
        """Test module model properties"""
        self.assertEqual(self.module.registered_students_count, 0)
        self.assertEqual(self.module.available_spots, 50)
        self.assertFalse(self.module.is_full)
        
        # Create registration
        Registration.objects.create(student=self.student, module=self.module)
        
        # Refresh from database
        self.module.refresh_from_db()
        self.assertEqual(self.module.registered_students_count, 1)
        self.assertEqual(self.module.available_spots, 49)
    
    def test_unique_registration_constraint(self):
        """Test that a student can only register once per module"""
        # Create first registration
        Registration.objects.create(student=self.student, module=self.module)
        
        # Try to create duplicate registration - should raise exception
        with self.assertRaises(Exception):
            Registration.objects.create(student=self.student, module=self.module)
