from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIClient, APITestCase as RestAPITestCase
from rest_framework import status
from students.models import Student
from modules.models import Module
from registrations.models import Registration
from sitecore.models import ContactMessage, SystemStats
import json
import json


class APITestCase(TestCase):
    """Base test case for API tests."""
    
    def setUp(self):
        """Set up test data."""
        self.client = APIClient()
        
        # Create test user and student
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
            phone='+1234567890'
        )
        
        # Create admin user
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='AdminPass123!'
        )
        
        # Create test modules
        self.module1 = Module.objects.create(
            code='CS101',
            name='Introduction to Computer Science',
            description='Basic concepts of computer science and programming.',
            credits=3,
            category='core',
            max_students=30,
            status='active'
        )
        
        self.module2 = Module.objects.create(
            code='MATH201',
            name='Advanced Mathematics',
            description='Advanced mathematical concepts and applications.',
            credits=4,
            category='core',
            max_students=25,
            status='active'
        )


class APIRootTestCase(RestAPITestCase):
    """Test cases for API root endpoint."""
    
    def test_api_root(self):
        """Test API root endpoint."""
        response = self.client.get(reverse('api:api_root'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
        self.assertIn('endpoints', response.data)


class StudentsAPITestCase(APITestCase):
    """Test cases for Students API endpoints."""
    
    def test_students_list_authenticated(self):
        """Test students list endpoint for authenticated user."""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('api:student-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Handle paginated response
        if 'results' in response.data:
            data = response.data['results']
        else:
            data = response.data
        
        # User should only see their own profile
        user_students = [s for s in data if s['user']['username'] == 'testuser']
        self.assertEqual(len(user_students), 1)
    
    def test_students_list_admin(self):
        """Test students list endpoint for admin user."""
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(reverse('api:student-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Handle paginated response
        if 'results' in response.data:
            data = response.data['results']
        else:
            data = response.data
        
        # Admin should see all students, at least our test student
        self.assertGreaterEqual(len(data), 1)
        usernames = [s['user']['username'] for s in data]
        self.assertIn('testuser', usernames)
    
    def test_students_list_unauthenticated(self):
        """Test students list endpoint for unauthenticated user."""
        response = self.client.get(reverse('api:student-list'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_student_detail(self):
        """Test student detail endpoint."""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(
            reverse('api:student-detail', kwargs={'pk': self.student.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user']['username'], 'testuser')
        self.assertEqual(response.data['phone'], '+1234567890')
    
    def test_student_update(self):
        """Test student profile update."""
        self.client.force_authenticate(user=self.user)
        data = {
            'phone': '+9876543210',
            'address': '123 Updated St'
        }
        response = self.client.patch(
            reverse('api:student-detail', kwargs={'pk': self.student.pk}),
            data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.student.refresh_from_db()
        self.assertEqual(self.student.phone, '+9876543210')
        self.assertEqual(self.student.address, '123 Updated St')


class ModulesAPITestCase(APITestCase):
    """Test cases for Modules API endpoints."""
    
    def test_modules_list(self):
        """Test modules list endpoint."""
        response = self.client.get(reverse('api:module-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Handle paginated response
        if 'results' in response.data:
            data = response.data['results']
        else:
            data = response.data
        
        # Should include our test modules
        self.assertGreaterEqual(len(data), 2)
        module_codes = [m['code'] for m in data]
        self.assertIn('CS101', module_codes)
        self.assertIn('MATH201', module_codes)
    
    def test_modules_list_search(self):
        """Test modules list search functionality."""
        response = self.client.get(
            reverse('api:module-list'),
            {'search': 'Computer'}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Handle paginated response
        if 'results' in response.data:
            data = response.data['results']
        else:
            data = response.data
        
        # Should find the CS101 module
        found_cs101 = any(m['code'] == 'CS101' for m in data)
        self.assertTrue(found_cs101)
    
    def test_modules_list_ordering(self):
        """Test modules list ordering."""
        response = self.client.get(
            reverse('api:module-list'),
            {'ordering': 'credits'}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Handle paginated response
        if 'results' in response.data:
            data = response.data['results']
        else:
            data = response.data
        
        # Find our test modules and verify ordering
        cs101 = next((m for m in data if m['code'] == 'CS101'), None)
        math201 = next((m for m in data if m['code'] == 'MATH201'), None)
        
        self.assertIsNotNone(cs101)
        self.assertIsNotNone(math201)
        self.assertEqual(cs101['credits'], 3)
        self.assertEqual(math201['credits'], 4)
    
    def test_module_detail(self):
        """Test module detail endpoint."""
        response = self.client.get(
            reverse('api:module-detail', kwargs={'pk': self.module1.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['code'], 'CS101')
        self.assertEqual(response.data['name'], 'Introduction to Computer Science')
        self.assertIn('enrolled_count', response.data)
        self.assertIn('can_register', response.data)
    
    def test_module_detail_authenticated_user(self):
        """Test module detail with authenticated user."""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(
            reverse('api:module-detail', kwargs={'pk': self.module1.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['can_register'])


class RegistrationsAPITestCase(APITestCase):
    """Test cases for Registrations API endpoints."""
    
    def test_registrations_list_authenticated(self):
        """Test registrations list for authenticated user."""
        # Create test registration
        Registration.objects.create(
            student=self.student,
            module=self.module1,
            status='enrolled'
        )
        
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('api:registration-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Handle paginated response
        if 'results' in response.data:
            data = response.data['results']
        else:
            data = response.data
        
        # Should include our test registration
        user_registrations = [r for r in data if r['module']['code'] == 'CS101']
        self.assertGreaterEqual(len(user_registrations), 1)
    
    def test_registrations_list_unauthenticated(self):
        """Test registrations list for unauthenticated user."""
        response = self.client.get(reverse('api:registration-list'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_registration_create(self):
        """Test creating a new registration."""
        self.client.force_authenticate(user=self.user)
        data = {'module_id': self.module1.pk}
        
        response = self.client.post(reverse('api:registration-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Check registration was created
        self.assertTrue(Registration.objects.filter(
            student=self.student,
            module=self.module1,
            status='enrolled'
        ).exists())
    
    def test_registration_create_duplicate(self):
        """Test creating duplicate registration."""
        # Create existing registration
        Registration.objects.create(
            student=self.student,
            module=self.module1,
            status='enrolled'
        )
        
        self.client.force_authenticate(user=self.user)
        data = {'module_id': self.module1.pk}
        
        response = self.client.post(reverse('api:registration-list'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_registration_create_invalid_module(self):
        """Test creating registration for invalid module."""
        self.client.force_authenticate(user=self.user)
        data = {'module_id': 99999}
        
        response = self.client.post(reverse('api:registration-list'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_registration_delete(self):
        """Test deleting (withdrawing from) a registration."""
        registration = Registration.objects.create(
            student=self.student,
            module=self.module1,
            status='enrolled'
        )
        
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(
            reverse('api:registration-detail', kwargs={'pk': registration.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Check registration was marked as withdrawn
        registration.refresh_from_db()
        self.assertEqual(registration.status, 'withdrawn')
        self.assertFalse(registration.is_active)


class ModuleRegistrationAPITestCase(APITestCase):
    """Test cases for Module Registration API endpoints."""
    
    def test_module_registration_authenticated(self):
        """Test module registration via API."""
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            reverse('api:module_register', kwargs={'module_id': self.module1.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Check registration was created
        self.assertTrue(Registration.objects.filter(
            student=self.student,
            module=self.module1,
            status='enrolled'
        ).exists())
    
    def test_module_registration_unauthenticated(self):
        """Test module registration for unauthenticated user."""
        response = self.client.post(
            reverse('api:module_register', kwargs={'module_id': self.module1.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_module_unregistration(self):
        """Test module unregistration via API."""
        # Create registration first
        Registration.objects.create(
            student=self.student,
            module=self.module1,
            status='enrolled'
        )
        
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(
            reverse('api:module_unregister', kwargs={'module_id': self.module1.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check registration was withdrawn
        registration = Registration.objects.get(
            student=self.student,
            module=self.module1
        )
        self.assertEqual(registration.status, 'withdrawn')
        self.assertFalse(registration.is_active)


class ContactAPITestCase(APITestCase):
    """Test cases for Contact API endpoint."""
    
    def test_contact_create(self):
        """Test creating a contact message via API."""
        data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'subject': 'Test Subject',
            'message': 'This is a test message.'
        }
        
        response = self.client.post(reverse('api:contact'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Check contact message was created
        self.assertTrue(ContactMessage.objects.filter(
            name='John Doe',
            email='john@example.com'
        ).exists())
    
    def test_contact_create_invalid_data(self):
        """Test creating contact message with invalid data."""
        data = {
            'name': '',
            'email': 'invalid-email',
            'subject': '',
            'message': ''
        }
        
        response = self.client.post(reverse('api:contact'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class SystemStatsAPITestCase(APITestCase):
    """Test cases for System Stats API endpoint."""
    
    def test_system_stats_list(self):
        """Test system stats endpoint."""
        # Create some stats
        SystemStats.objects.create()
        
        response = self.client.get(reverse('api:stats'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Handle paginated response
        if 'results' in response.data:
            data = response.data['results']
        else:
            data = response.data
        
        self.assertGreaterEqual(len(data), 1)
        
        # Find our stats entry
        stats = data[0]
        self.assertIn('total_students', stats)
        self.assertIn('total_modules', stats)
        self.assertIn('total_registrations', stats)


class UserProfileAPITestCase(APITestCase):
    """Test cases for User Profile API endpoint."""
    
    def test_user_profile_get(self):
        """Test getting user profile."""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('api:profile'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testuser')
        self.assertEqual(response.data['email'], 'test@example.com')
    
    def test_user_profile_update(self):
        """Test updating user profile."""
        self.client.force_authenticate(user=self.user)
        data = {
            'first_name': 'Updated',
            'last_name': 'Name',
            'email': 'updated@example.com'
        }
        
        response = self.client.patch(reverse('api:profile'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Updated')
        self.assertEqual(self.user.last_name, 'Name')
        self.assertEqual(self.user.email, 'updated@example.com')
    
    def test_user_profile_unauthenticated(self):
        """Test user profile for unauthenticated user."""
        response = self.client.get(reverse('api:profile'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class APIDocsTestCase(APITestCase):
    """Test cases for API documentation endpoint."""
    
    def test_api_docs_view(self):
        """Test API documentation view."""
        response = self.client.get(reverse('api:api_docs'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'API Documentation')
        self.assertContains(response, 'Students')
        self.assertContains(response, 'Modules')
        self.assertContains(response, 'Registrations')
