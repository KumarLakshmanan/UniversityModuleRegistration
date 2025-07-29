from django.test import TestCase, Client
from django.urls import reverse
from django.core import mail
from .models import ContactMessage, SystemStats
from students.models import Student
from modules.models import Module
from registrations.models import Registration
from django.contrib.auth.models import User


class SitecoreViewsTestCase(TestCase):
    """Test cases for sitecore app views."""
    
    def setUp(self):
        """Set up test data."""
        self.client = Client()
    
    def test_home_view(self):
        """Test home page view."""
        response = self.client.get(reverse('sitecore:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Course Module Registration System')
    
    def test_about_view(self):
        """Test about page view."""
        response = self.client.get(reverse('sitecore:about'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'About')
    
    def test_contact_view_get(self):
        """Test contact page GET request."""
        response = self.client.get(reverse('sitecore:contact'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Contact Us')
        self.assertContains(response, 'Name')
        self.assertContains(response, 'Email')
        self.assertContains(response, 'Subject')
        self.assertContains(response, 'Message')
    
    def test_contact_view_post_valid_data(self):
        """Test contact form submission with valid data."""
        data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'subject': 'Test Subject',
            'message': 'This is a test message.'
        }
        
        response = self.client.post(reverse('sitecore:contact'), data)
        self.assertEqual(response.status_code, 302)  # Redirect after success
        
        # Check that contact message was created
        self.assertTrue(ContactMessage.objects.filter(
            name='John Doe',
            email='john@example.com',
            subject='Test Subject'
        ).exists())
    
    def test_contact_view_post_invalid_data(self):
        """Test contact form submission with invalid data."""
        data = {
            'name': '',  # Required field
            'email': 'invalid-email',  # Invalid email
            'subject': 'Test Subject',
            'message': ''  # Required field
        }
        
        response = self.client.post(reverse('sitecore:contact'), data)
        self.assertEqual(response.status_code, 200)  # Stay on form with errors
        self.assertContains(response, 'This field is required')
    
    def test_contact_view_ajax_valid_data(self):
        """Test AJAX contact form submission with valid data."""
        data = {
            'name': 'Jane Doe',
            'email': 'jane@example.com',
            'subject': 'AJAX Test',
            'message': 'This is an AJAX test message.'
        }
        
        response = self.client.post(
            reverse('sitecore:contact'),
            data,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        
        self.assertEqual(response.status_code, 200)
        json_response = response.json()
        self.assertTrue(json_response['success'])
        self.assertIn('Thank you', json_response['message'])
        
        # Check that contact message was created
        self.assertTrue(ContactMessage.objects.filter(
            name='Jane Doe',
            email='jane@example.com'
        ).exists())
    
    def test_contact_view_ajax_invalid_data(self):
        """Test AJAX contact form submission with invalid data."""
        data = {
            'name': '',
            'email': 'invalid-email',
            'subject': '',
            'message': ''
        }
        
        response = self.client.post(
            reverse('sitecore:contact'),
            data,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        
        self.assertEqual(response.status_code, 400)
        json_response = response.json()
        self.assertFalse(json_response['success'])
        self.assertIn('errors', json_response)
    
    def test_unauthorized_view(self):
        """Test unauthorized access page."""
        response = self.client.get(reverse('sitecore:unauthorized'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Unauthorized')
        self.assertContains(response, 'Access Denied')
    
    def test_home_view_context_data(self):
        """Test home view context data."""
        # Create some test data
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='TestPass123!'
        )
        student = Student.objects.create(user=user, is_verified=True)
        
        module = Module.objects.create(
            code='CS101',
            name='Computer Science 101',
            description='Basic CS course',
            credits=3,
            category='core',
            max_students=30
        )
        
        Registration.objects.create(
            student=student,
            module=module,
            status='enrolled'
        )
        
        response = self.client.get(reverse('sitecore:home'))
        context = response.context
        
        self.assertIn('stats', context)
        stats = context['stats']
        self.assertEqual(stats['total_students'], 1)
        self.assertEqual(stats['total_modules'], 1)
        self.assertEqual(stats['total_registrations'], 1)


class ContactMessageModelTestCase(TestCase):
    """Test cases for ContactMessage model."""
    
    def test_contact_message_creation(self):
        """Test contact message creation."""
        message = ContactMessage.objects.create(
            name='Test User',
            email='test@example.com',
            subject='Test Subject',
            message='This is a test message.'
        )
        
        self.assertEqual(message.name, 'Test User')
        self.assertEqual(message.email, 'test@example.com')
        self.assertEqual(message.subject, 'Test Subject')
        self.assertFalse(message.is_resolved)  # Default value
        self.assertIsNotNone(message.created_at)
    
    def test_contact_message_string_representation(self):
        """Test ContactMessage __str__ method."""
        message = ContactMessage.objects.create(
            name='John Doe',
            email='john@example.com',
            subject='Help Request',
            message='I need help with registration.'
        )
        
        expected = 'John Doe - Help Request'
        self.assertEqual(str(message), expected)
    
    def test_contact_message_resolution(self):
        """Test contact message resolution."""
        message = ContactMessage.objects.create(
            name='Test User',
            email='test@example.com',
            subject='Test Subject',
            message='Test message'
        )
        
        # Initially not resolved
        self.assertFalse(message.is_resolved)
        
        # Mark as resolved
        message.is_resolved = True
        message.save()
        
        message.refresh_from_db()
        self.assertTrue(message.is_resolved)
    
    def test_contact_message_ordering(self):
        """Test contact message model ordering."""
        # Create multiple messages
        msg1 = ContactMessage.objects.create(
            name='User 1',
            email='user1@example.com',
            subject='Subject 1',
            message='Message 1'
        )
        
        msg2 = ContactMessage.objects.create(
            name='User 2',
            email='user2@example.com',
            subject='Subject 2',
            message='Message 2'
        )
        
        # Check ordering (should be by date_created descending)
        messages = ContactMessage.objects.all()
        self.assertEqual(messages[0], msg2)  # Most recent first
        self.assertEqual(messages[1], msg1)


class SystemStatsModelTestCase(TestCase):
    """Test cases for SystemStats model."""
    
    def setUp(self):
        """Set up test data."""
        # Create test users and students
        self.user1 = User.objects.create_user(
            username='user1',
            email='user1@example.com',
            password='TestPass123!'
        )
        self.student1 = Student.objects.create(user=self.user1, is_verified=True)
        
        self.user2 = User.objects.create_user(
            username='user2',
            email='user2@example.com',
            password='TestPass123!'
        )
        self.student2 = Student.objects.create(user=self.user2, is_verified=True)
        
        # Create test modules
        self.module1 = Module.objects.create(
            code='CS101',
            name='Computer Science 101',
            description='Basic CS course',
            credits=3,
            category='core',
            max_students=30
        )
        
        self.module2 = Module.objects.create(
            code='MATH101',
            name='Mathematics 101',
            description='Basic Math course',
            credits=4,
            category='core',
            max_students=25
        )
        
        # Create test registrations
        Registration.objects.create(
            student=self.student1,
            module=self.module1,
            status='enrolled'
        )
        
        Registration.objects.create(
            student=self.student2,
            module=self.module1,
            status='completed'
        )
        
        Registration.objects.create(
            student=self.student1,
            module=self.module2,
            status='enrolled'
        )
    
    def test_system_stats_creation(self):
        """Test system stats creation."""
        stats = SystemStats.objects.create()
        
        self.assertEqual(stats.total_students, 2)
        self.assertEqual(stats.total_modules, 2)
        self.assertEqual(stats.total_registrations, 3)
        self.assertEqual(stats.active_registrations, 2)  # enrolled registrations
        self.assertEqual(stats.completed_registrations, 1)  # completed registrations
        self.assertIsNotNone(stats.date_recorded)
    
    def test_system_stats_string_representation(self):
        """Test SystemStats __str__ method."""
        stats = SystemStats.objects.create()
        
        expected_start = f"Stats for {stats.date_recorded.strftime('%Y-%m-%d')}"
        self.assertTrue(str(stats).startswith(expected_start))
    
    def test_system_stats_update_method(self):
        """Test system stats update_stats method."""
        stats = SystemStats()
        stats.update_stats()
        
        self.assertEqual(stats.total_students, 2)
        self.assertEqual(stats.total_modules, 2)
        self.assertEqual(stats.total_registrations, 3)
        self.assertEqual(stats.active_registrations, 2)
        self.assertEqual(stats.completed_registrations, 1)
    
    def test_system_stats_with_inactive_data(self):
        """Test system stats with inactive modules and withdrawn registrations."""
        # Create inactive module
        inactive_module = Module.objects.create(
            code='OLD101',
            name='Old Course',
            description='Inactive course',
            credits=2,
            category='core',
            max_students=20,
            status='inactive'
        )
        
        # Create withdrawn registration
        Registration.objects.create(
            student=self.student2,
            module=self.module2,
            status='withdrawn',
            is_active=False
        )
        
        stats = SystemStats.objects.create()
        
        # Should only count active modules and registrations
        self.assertEqual(stats.total_modules, 2)  # Only active modules
        self.assertEqual(stats.total_registrations, 4)  # All registrations
        self.assertEqual(stats.active_registrations, 2)  # Only active enrolled
    
    def test_system_stats_ordering(self):
        """Test system stats model ordering."""
        # Create multiple stats entries
        stats1 = SystemStats.objects.create()
        stats2 = SystemStats.objects.create()
        
        # Check ordering (should be by date_recorded descending)
        all_stats = SystemStats.objects.all()
        self.assertEqual(all_stats[0], stats2)  # Most recent first
        self.assertEqual(all_stats[1], stats1)
