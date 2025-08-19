from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from .models import Course, Module
from students.models import Student
from registrations.models import Registration


class ModulesViewsTestCase(TestCase):
    """Test cases for modules app views."""
    
    def setUp(self):
        """Set up test data."""
        self.client = Client()
        
        # Create test user and student
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='TestPass123!'
        )
        self.student = Student.objects.create(
            user=self.user,
            is_verified=True
        )
        
        # Create test courses
        self.course1 = Course.objects.create(
            title='Computer Science Program',
            course_code='CS-PROG',
            description='Comprehensive computer science program',
            status='active'
        )
        
        self.course2 = Course.objects.create(
            title='Mathematics Program',
            course_code='MATH-PROG',
            description='Advanced mathematics program',
            status='active'
        )
        
        # Create test modules
        self.module1 = Module.objects.create(
            course=self.course1,
            code='CS101',
            name='Introduction to Computer Science',
            description='Basic concepts of computer science and programming.',
            credits=3,
            category='core',
            max_students=30,
            status='active'
        )
        
        self.module2 = Module.objects.create(
            course=self.course2,
            code='MATH201',
            name='Advanced Mathematics',
            description='Advanced mathematical concepts and applications.',
            credits=4,
            category='core',
            max_students=25,
            status='active'
        )
        
        self.inactive_module = Module.objects.create(
            course=self.course1,
            code='OLD101',
            name='Inactive Module',
            description='This module is inactive.',
            credits=2,
            category='elective',
            max_students=20,
            status='inactive'
        )
    
    def test_module_list_view(self):
        """Test module list view - now redirects to course list."""
        response = self.client.get(reverse('modules:list'))
        self.assertEqual(response.status_code, 302)  # Redirects to course list
        
        # Test course list instead
        response = self.client.get(reverse('modules:course_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Course Catalog')
        self.assertContains(response, self.course1.title)
        self.assertContains(response, self.course2.title)
    
    def test_module_list_search(self):
        """Test course list search functionality."""
        response = self.client.get(reverse('modules:course_list'), {'search': 'Computer'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.course1.title)
        self.assertNotContains(response, self.course2.title)
    
    def test_module_list_category_filter(self):
        """Test course list available filter."""
        response = self.client.get(reverse('modules:course_list'), {'available': 'true'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.course1.title)
        self.assertContains(response, self.course2.title)  # Both are available
    
    def test_module_detail_view(self):
        """Test module detail view."""
        response = self.client.get(reverse('modules:detail', kwargs={'code': self.module1.code}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.module1.name)
        self.assertContains(response, self.module1.description)
        self.assertContains(response, str(self.module1.credits))
    
    def test_module_detail_view_nonexistent(self):
        """Test module detail view for nonexistent module."""
        response = self.client.get(reverse('modules:detail', kwargs={'code': 'NONEXISTENT'}))
        self.assertEqual(response.status_code, 404)
    
    def test_module_detail_registration_button_authenticated(self):
        """Test registration button visibility for authenticated users."""
        self.client.login(username='testuser', password='TestPass123!')
        response = self.client.get(reverse('modules:detail', kwargs={'code': self.module1.code}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Register for Course')
    
    def test_module_detail_registration_button_unauthenticated(self):
        """Test registration button visibility for unauthenticated users."""
        response = self.client.get(reverse('modules:detail', kwargs={'code': self.module1.code}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Login to Register')
    
    def test_module_detail_already_registered(self):
        """Test module detail view when already registered."""
        # Create registration
        Registration.objects.create(
            student=self.student,
            module=self.module1,
            status='enrolled'
        )
        
        self.client.login(username='testuser', password='TestPass123!')
        response = self.client.get(reverse('modules:detail', kwargs={'code': self.module1.code}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Unregister from Course')
    
    def test_module_detail_context_data(self):
        """Test module detail view context data."""
        self.client.login(username='testuser', password='TestPass123!')
        response = self.client.get(reverse('modules:detail', kwargs={'code': self.module1.code}))
        
        context = response.context
        self.assertIn('module', context)
        self.assertIn('course_modules', context)
        self.assertIn('course', context)
        self.assertIn('user_registered', context)
        
        self.assertEqual(context['module'], self.module1)
        self.assertEqual(context['course'], self.course1)
        self.assertFalse(context['user_registered'])  # No registration yet
    
    def test_module_registration_ajax_authenticated(self):
        """Test AJAX module registration for authenticated user."""
        self.client.login(username='testuser', password='TestPass123!')
        
        response = self.client.post(
            reverse('modules:register', kwargs={'pk': self.module1.pk}),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])
        self.assertIn('Successfully registered', data['message'])
        
        # Check registration was created
        self.assertTrue(Registration.objects.filter(
            student=self.student,
            module=self.module1,
            status='enrolled'
        ).exists())
    
    def test_module_registration_ajax_unauthenticated(self):
        """Test AJAX module registration for unauthenticated user."""
        response = self.client.post(
            reverse('modules:register', kwargs={'pk': self.module1.pk}),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        
        self.assertEqual(response.status_code, 302)  # Redirect to login
        # No JSON response expected for redirect
    
    def test_module_registration_ajax_duplicate(self):
        """Test AJAX module registration for already registered module."""
        # Create existing registration
        Registration.objects.create(
            student=self.student,
            module=self.module1,
            status='enrolled'
        )
        
        self.client.login(username='testuser', password='TestPass123!')
        
        response = self.client.post(
            reverse('modules:register', kwargs={'pk': self.module1.pk}),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        
        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertFalse(data['success'])
        self.assertIn('already registered', data['message'])
    
    def test_module_unregistration_ajax(self):
        """Test AJAX module unregistration."""
        # Create registration first
        registration = Registration.objects.create(
            student=self.student,
            module=self.module1,
            status='enrolled'
        )
        
        self.client.login(username='testuser', password='TestPass123!')
        
        response = self.client.post(
            reverse('modules:unregister', kwargs={'pk': self.module1.pk}),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])
        
        # Check registration was marked as withdrawn
        registration.refresh_from_db()
        self.assertEqual(registration.status, 'withdrawn')
        self.assertFalse(registration.is_active)
    
    def test_module_list_pagination(self):
        """Test course list pagination."""
        # Create many courses to test pagination
        for i in range(15):
            course = Course.objects.create(
                title=f'Test Course {i}',
                course_code=f'TEST{i:03d}',
                description='Test description',
                status='active'
            )
            Module.objects.create(
                course=course,
                code=f'MOD{i:03d}',
                name=f'Test Module {i}',
                description='Test description',
                credits=3,
                category='core',
                max_students=30,
                status='active'
            )
        
        response = self.client.get(reverse('modules:course_list'))
        self.assertEqual(response.status_code, 200)
        
        # Should show pagination
        self.assertContains(response, 'pagination')


class ModuleModelTestCase(TestCase):
    """Test cases for Module model."""
    
    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='TestPass123!'
        )
        self.student = Student.objects.create(
            user=self.user,
            is_verified=True
        )
        
        # Create test course
        self.course = Course.objects.create(
            title='Computer Science Program',
            course_code='CS-PROG',
            description='Comprehensive computer science program',
            status='active'
        )
        
        self.module = Module.objects.create(
            course=self.course,
            code='CS101',
            name='Computer Science 101',
            description='Basic computer science course',
            credits=3,
            category='core',
            max_students=30,
            status='active'
        )
    
    def test_module_creation(self):
        """Test module creation."""
        self.assertEqual(self.module.code, 'CS101')
        self.assertEqual(self.module.name, 'Computer Science 101')
        self.assertEqual(self.module.credits, 3)
        self.assertEqual(self.module.status, 'active')
    
    def test_module_string_representation(self):
        """Test module __str__ method."""
        expected = 'CS-PROG-CS101 - Computer Science 101'
        self.assertEqual(str(self.module), expected)
    
    def test_module_is_registration_open_property(self):
        """Test is_registration_open property."""
        # Module should be available for registration
        self.assertTrue(self.module.is_available_for_registration)
        
        # Module with closed registration should not be open
        closed_module = Module.objects.create(
            course=self.course,
            code='CLOSED101',
            name='Closed Module',
            description='Closed module',
            credits=2,
            category='elective',
            max_students=20,
            status='active',
            is_available_for_registration=False
        )
        self.assertFalse(closed_module.is_available_for_registration)
    
    def test_module_can_register_method(self):
        """Test can_register method."""
        # Should be able to register for new module
        self.assertTrue(self.module.can_register())
        
        # Should not be able to register if already registered
        Registration.objects.create(
            student=self.student,
            module=self.module,
            status='enrolled'
        )
        # Note: can_register() doesn't check individual student registration
        # That's handled in the serializer/view logic
        self.assertTrue(self.module.can_register())
    
    def test_module_can_register_full_module(self):
        """Test can_register method for full module."""
        # Set max_students to 1
        self.module.max_students = 1
        self.module.save()
        
        # Create another student and register them
        other_user = User.objects.create_user(
            username='otheruser',
            email='other@example.com',
            password='TestPass123!'
        )
        other_student = Student.objects.create(
            user=other_user,
            is_verified=True
        )
        
        Registration.objects.create(
            student=other_student,
            module=self.module,
            status='enrolled'
        )
        
        # Now original student should not be able to register
        self.assertFalse(self.module.can_register())
    
    def test_module_can_register_inactive_module(self):
        """Test can_register method for inactive module."""
        self.module.status = 'inactive'
        self.module.save()
        
        self.assertFalse(self.module.can_register())
    
    def test_module_enrolled_students_count(self):
        """Test enrolled students count."""
        # Initially no enrolled students
        enrolled_count = self.module.enrolled_students_count
        self.assertEqual(enrolled_count, 0)
        
        # Add enrolled student
        Registration.objects.create(
            student=self.student,
            module=self.module,
            status='enrolled'
        )
        
        enrolled_count = self.module.enrolled_students_count
        self.assertEqual(enrolled_count, 1)
    
    def test_module_code_uniqueness(self):
        """Test module code uniqueness."""
        from django.db import IntegrityError
        
        with self.assertRaises(IntegrityError):
            Module.objects.create(
                course=self.course,
                code='CS101',  # Duplicate code within same course
                name='Another CS Course',
                description='Another course',
                credits=4,
                category='core',
                max_students=25,
                status='active'
            )
