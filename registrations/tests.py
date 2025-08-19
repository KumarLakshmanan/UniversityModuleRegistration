from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from .models import Registration
from students.models import Student
from modules.models import Course, Module


class RegistrationsViewsTestCase(TestCase):
    """Test cases for registrations app views."""
    
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
        
        # Create test course
        self.course = Course.objects.create(
            title='Computer Science Program',
            course_code='CS-PROG',
            description='Comprehensive computer science program',
            status='active'
        )
        
        # Create test modules
        self.module1 = Module.objects.create(
            course=self.course,
            code='CS101',
            name='Computer Science 101',
            description='Basic computer science course',
            credits=3,
            category='core',
            max_students=30,
            status='active'
        )
        
        self.module2 = Module.objects.create(
            course=self.course,
            code='MATH201',
            name='Advanced Mathematics',
            description='Advanced mathematical concepts',
            credits=4,
            category='core',
            max_students=25,
            status='active'
        )
        
        # Create test registrations
        self.registration1 = Registration.objects.create(
            student=self.student,
            module=self.module1,
            status='enrolled'
        )
        
        self.registration2 = Registration.objects.create(
            student=self.student,
            module=self.module2,
            status='completed',
            grade='A'
        )
    
    def test_my_modules_view_authenticated(self):
        """Test my modules view for authenticated user."""
        self.client.login(username='testuser', password='TestPass123!')
        response = self.client.get(reverse('registrations:my_modules'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'My Registered Modules')
        self.assertContains(response, self.module1.name)
        self.assertContains(response, self.module2.name)
    
    def test_my_modules_view_unauthenticated(self):
        """Test my modules view for unauthenticated user."""
        response = self.client.get(reverse('registrations:my_modules'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
    
    def test_my_modules_view_context_data(self):
        """Test my modules view context data."""
        self.client.login(username='testuser', password='TestPass123!')
        response = self.client.get(reverse('registrations:my_modules'))
        
        context = response.context
        self.assertIn('student', context)
        self.assertIn('total_credits', context)
        self.assertIn('status_counts', context)
        
        # Check values
        self.assertEqual(context['student'], self.student)
        self.assertEqual(context['total_credits'], 7)  # 3 + 4 credits
        
        status_counts = context['status_counts']
        self.assertEqual(status_counts['enrolled'], 1)
        self.assertEqual(status_counts['completed'], 1)
    
    def test_my_modules_view_empty_state(self):
        """Test my modules view with no registrations."""
        # Create new user with no registrations
        new_user = User.objects.create_user(
            username='newuser',
            email='new@example.com',
            password='NewPass123!'
        )
        new_student = Student.objects.create(
            user=new_user,
            is_verified=True
        )
        
        self.client.login(username='newuser', password='NewPass123!')
        response = self.client.get(reverse('registrations:my_modules'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No Modules Registered')
        self.assertContains(response, 'Browse Courses')
    
    def test_my_modules_view_pagination(self):
        """Test my modules view pagination."""
        # Create many registrations to test pagination
        for i in range(15):
            module = Module.objects.create(
                course=self.course,
                code=f'TEST{i:03d}',
                name=f'Test Module {i}',
                description='Test description',
                credits=2,
                category='core',
                max_students=30,
                status='active'
            )
            Registration.objects.create(
                student=self.student,
                module=module,
                status='enrolled'
            )
        
        self.client.login(username='testuser', password='TestPass123!')
        response = self.client.get(reverse('registrations:my_modules'))
        self.assertEqual(response.status_code, 200)
        
        # Should show pagination
        self.assertContains(response, 'pagination')
    
    def test_my_modules_view_only_active_registrations(self):
        """Test that only active registrations are shown."""
        # Create inactive registration
        inactive_module = Module.objects.create(
            course=self.course,
            code='INACTIVE',
            name='Inactive Module',
            description='Inactive module',
            credits=1,
            category='elective',
            max_students=30,
            status='active'
        )
        
        inactive_registration = Registration.objects.create(
            student=self.student,
            module=inactive_module,
            status='withdrawn',
            is_active=False
        )
        
        self.client.login(username='testuser', password='TestPass123!')
        response = self.client.get(reverse('registrations:my_modules'))
        
        # Should not show inactive registration
        self.assertNotContains(response, inactive_module.name)
        
        # Should still show active registrations
        self.assertContains(response, self.module1.name)
        self.assertContains(response, self.module2.name)
    
    def test_my_modules_queryset_optimization(self):
        """Test that the view uses optimized querysets."""
        self.client.login(username='testuser', password='TestPass123!')
        
        with self.assertNumQueries(8):  # Should be efficient with select_related
            response = self.client.get(reverse('registrations:my_modules'))
            
        self.assertEqual(response.status_code, 200)


class RegistrationModelTestCase(TestCase):
    """Test cases for Registration model."""
    
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
    
    def test_registration_creation(self):
        """Test registration creation."""
        registration = Registration.objects.create(
            student=self.student,
            module=self.module,
            status='enrolled'
        )
        
        self.assertEqual(registration.student, self.student)
        self.assertEqual(registration.module, self.module)
        self.assertEqual(registration.status, 'enrolled')
        self.assertTrue(registration.is_active)
        self.assertIsNotNone(registration.date_registered)
    
    def test_registration_string_representation(self):
        """Test registration __str__ method."""
        registration = Registration.objects.create(
            student=self.student,
            module=self.module,
            status='enrolled'
        )
        
        expected = f"{self.student.get_full_name()} - CS-PROG-CS101"
        self.assertEqual(str(registration), expected)
    
    def test_registration_default_values(self):
        """Test registration default field values."""
        registration = Registration.objects.create(
            student=self.student,
            module=self.module
        )
        
        self.assertEqual(registration.status, 'enrolled')  # Default status
        self.assertTrue(registration.is_active)  # Default active
        self.assertIsNone(registration.grade)  # No grade initially
        self.assertIsNone(registration.completion_date)  # No completion date
    
    def test_registration_status_choices(self):
        """Test registration status choices."""
        registration = Registration.objects.create(
            student=self.student,
            module=self.module,
            status='completed'
        )
        
        self.assertEqual(registration.status, 'completed')
        self.assertEqual(registration.get_status_display(), 'Completed')
        
        # Test other status choices
        registration.status = 'withdrawn'
        registration.save()
        self.assertEqual(registration.get_status_display(), 'Withdrawn')
    
    def test_registration_completion(self):
        """Test registration completion."""
        registration = Registration.objects.create(
            student=self.student,
            module=self.module,
            status='enrolled'
        )
        
        # Complete the registration
        completion_date = timezone.now().date()
        registration.status = 'completed'
        registration.grade = 'A'
        registration.date_completed = completion_date
        registration.save()
        
        registration.refresh_from_db()
        self.assertEqual(registration.status, 'completed')
        self.assertEqual(registration.grade, 'A')
        self.assertEqual(registration.date_completed, completion_date)
    
    def test_registration_withdrawal(self):
        """Test registration withdrawal."""
        registration = Registration.objects.create(
            student=self.student,
            module=self.module,
            status='enrolled'
        )
        
        # Withdraw the registration
        registration.status = 'withdrawn'
        registration.is_active = False
        registration.save()
        
        registration.refresh_from_db()
        self.assertEqual(registration.status, 'withdrawn')
        self.assertFalse(registration.is_active)
    
    def test_registration_unique_together(self):
        """Test that student can't register for same module twice."""
        # Create first registration
        Registration.objects.create(
            student=self.student,
            module=self.module,
            status='enrolled'
        )
        
        # Try to create duplicate registration
        from django.db import IntegrityError
        with self.assertRaises(IntegrityError):
            Registration.objects.create(
                student=self.student,
                module=self.module,
                status='enrolled'
            )
    
    def test_registration_ordering(self):
        """Test registration model ordering."""
        # Import timezone for explicit date setting
        from django.utils import timezone
        import datetime
        
        # Create multiple registrations with different dates
        reg1 = Registration.objects.create(
            student=self.student,
            module=self.module,
            status='enrolled'
        )
        
        # Create another module and registration
        module2 = Module.objects.create(
            course=self.course,
            code='MATH101',
            name='Mathematics 101',
            description='Basic mathematics',
            credits=4,
            category='core',
            max_students=30,
            status='active'
        )
        
        reg2 = Registration.objects.create(
            student=self.student,
            module=module2,
            status='enrolled'
        )
        
        # Update date_registered to ensure ordering
        reg2.date_registered = timezone.now() + datetime.timedelta(seconds=1)
        reg2.save()
        
        # Check ordering (should be by date_registered descending)
        registrations = Registration.objects.filter(student=self.student)
        self.assertEqual(registrations[0], reg2)  # Most recent first
        self.assertEqual(registrations[1], reg1)
    
    def test_registration_grade_choices(self):
        """Test registration grade choices."""
        registration = Registration.objects.create(
            student=self.student,
            module=self.module,
            status='completed',
            grade='A+'
        )
        
        self.assertEqual(registration.grade, 'A+')
        
        # Test other valid grades
        valid_grades = ['A+', 'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-', 'D', 'F']
        for grade in valid_grades:
            registration.grade = grade
            registration.save()
            registration.refresh_from_db()
            self.assertEqual(registration.grade, grade)
