from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from rest_framework import status
from students.models import Student
from modules.models import Module, Registration


class APITestCase(APITestCase):
    """Test cases for API endpoints"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='apiuser',
            email='api@example.com',
            password='apipass123'
        )
        self.student = Student.objects.create(
            user=self.user,
            date_of_birth='1990-01-01',
            address='123 API St',
            city='API City',
            country='API Country'
        )
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        self.module = Module.objects.create(
            name='API Test Module',
            code='API101',
            credit=4,
            description='API test module description',
            max_students=25
        )
        
        self.registration = Registration.objects.create(
            student=self.student,
            module=self.module
        )
    
    def test_modules_api_list(self):
        """Test modules API list endpoint"""
        response = self.client.get('/api/modules/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        self.assertIn('count', response.data)
    
    def test_modules_api_detail(self):
        """Test modules API detail endpoint"""
        response = self.client.get(f'/api/modules/{self.module.pk}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['code'], 'API101')
        self.assertEqual(response.data['name'], 'API Test Module')
    
    def test_students_api_list(self):
        """Test students API list endpoint"""
        response = self.client.get('/api/students/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
    
    def test_students_api_detail(self):
        """Test students API detail endpoint"""
        response = self.client.get(f'/api/students/{self.student.pk}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user']['username'], 'apiuser')
    
    def test_registrations_api_list(self):
        """Test registrations API list endpoint"""
        response = self.client.get('/api/registrations/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
    
    def test_registrations_api_detail(self):
        """Test registrations API detail endpoint"""
        response = self.client.get(f'/api/registrations/{self.registration.pk}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['student']['user']['username'], 'apiuser')
        self.assertEqual(response.data['module']['code'], 'API101')
    
    def test_external_data_api(self):
        """Test external data API endpoint"""
        response = self.client.get('/api/external-data/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('success', response.data)
    
    def test_api_pagination(self):
        """Test API pagination works"""
        response = self.client.get('/api/modules/?page=1&page_size=5')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        self.assertIn('count', response.data)
        self.assertIn('next', response.data)
        self.assertIn('previous', response.data)
    
    def test_api_search(self):
        """Test API search functionality"""
        response = self.client.get('/api/modules/?search=API')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
    
    def test_api_filtering(self):
        """Test API filtering functionality"""
        response = self.client.get('/api/modules/?category=core&credit=4')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
    
    def test_api_ordering(self):
        """Test API ordering functionality"""
        response = self.client.get('/api/modules/?ordering=name')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        
        response = self.client.get('/api/modules/?ordering=-name')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
    
    def test_api_without_auth(self):
        """Test API requires authentication"""
        client = APIClient()  # No authentication
        response = client.get('/api/modules/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_module_registrations_endpoint(self):
        """Test module registrations custom action"""
        response = self.client.get(f'/api/modules/{self.module.pk}/registrations/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
    
    def test_student_modules_endpoint(self):
        """Test student modules custom action"""
        response = self.client.get(f'/api/students/{self.student.pk}/modules/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
