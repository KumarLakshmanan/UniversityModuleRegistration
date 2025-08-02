from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from rest_framework import status
from students.models import Student
from modules.models import Module, Registration


class APITestCase(APITestCase):
    
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
        response = self.client.get('/api/modules/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        self.assertIn('count', response.data)
    
    def test_modules_api_detail(self):
        response = self.client.get(f'/api/modules/{self.module.pk}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['code'], 'API101')
        self.assertEqual(response.data['name'], 'API Test Module')
    
    def test_students_api_list(self):
        response = self.client.get('/api/students/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
    
    def test_students_api_detail(self):
        response = self.client.get(f'/api/students/{self.student.pk}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user']['username'], 'apiuser')
    
    def test_registrations_api_list(self):
        response = self.client.get('/api/registrations/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
    
    def test_registrations_api_detail(self):
        response = self.client.get(f'/api/registrations/{self.registration.pk}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['student']['user']['username'], 'apiuser')
        self.assertEqual(response.data['module']['code'], 'API101')
    
    def test_external_data_api(self):
        response = self.client.get('/api/external-data/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('success', response.data)
    
    def test_api_pagination(self):
        response = self.client.get('/api/modules/?page=1&page_size=5')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        self.assertIn('count', response.data)
        self.assertIn('next', response.data)
        self.assertIn('previous', response.data)
    
    def test_api_search(self):
        response = self.client.get('/api/modules/?search=API')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
    
    def test_api_filtering(self):
        response = self.client.get('/api/modules/?category=core&credit=4')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
    
    def test_api_ordering(self):
        response = self.client.get('/api/modules/?ordering=name')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        
        response = self.client.get('/api/modules/?ordering=-name')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
    
    def test_api_without_auth(self):
        client = APIClient()  # No authentication
        response = client.get('/api/modules/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_module_registrations_endpoint(self):
        response = self.client.get(f'/api/modules/{self.module.pk}/registrations/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
    
    def test_student_modules_endpoint(self):
        response = self.client.get(f'/api/students/{self.student.pk}/modules/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
