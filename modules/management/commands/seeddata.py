from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from modules.models import Module
from students.models import Student
from registrations.models import Registration
import random


class Command(BaseCommand):
    help = 'Seed the database with sample data for development and testing'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting data seeding...'))
        
        # Create sample modules
        self.create_sample_modules()
        
        # Create sample students (if needed)
        self.create_sample_students()
        
        # Create sample registrations
        self.create_sample_registrations()
        
        self.stdout.write(self.style.SUCCESS('Data seeding completed successfully!'))

    def create_sample_modules(self):
        """Create sample modules for testing."""
        modules_data = [
            {
                'name': 'Introduction to Computer Science',
                'code': 'CS101',
                'description': 'A comprehensive introduction to computer science concepts, programming fundamentals, and problem-solving techniques.',
                'credits': 3,
                'category': 'core',
                'prerequisites': 'None',
                'max_students': 50,
            },
            {
                'name': 'Web Development Fundamentals',
                'code': 'WEB201',
                'description': 'Learn the basics of web development including HTML, CSS, JavaScript, and modern web frameworks.',
                'credits': 4,
                'category': 'core',
                'prerequisites': 'CS101 or equivalent programming experience',
                'max_students': 30,
            },
            {
                'name': 'Database Systems',
                'code': 'DB301',
                'description': 'Study database design, SQL, normalization, and database management systems.',
                'credits': 3,
                'category': 'core',
                'prerequisites': 'CS101, basic understanding of data structures',
                'max_students': 40,
            },
            {
                'name': 'Machine Learning Basics',
                'code': 'ML401',
                'description': 'Introduction to machine learning algorithms, data preprocessing, and model evaluation.',
                'credits': 4,
                'category': 'elective',
                'prerequisites': 'Statistics, Python programming, Linear Algebra',
                'max_students': 25,
            },
            {
                'name': 'Mobile App Development',
                'code': 'MOB301',
                'description': 'Learn to develop mobile applications for iOS and Android platforms using modern frameworks.',
                'credits': 4,
                'category': 'elective',
                'prerequisites': 'WEB201 or equivalent programming experience',
                'max_students': 35,
            },
            {
                'name': 'Software Engineering Principles',
                'code': 'SE401',
                'description': 'Study software development lifecycle, design patterns, testing, and project management.',
                'credits': 3,
                'category': 'core',
                'prerequisites': 'CS101, WEB201',
                'max_students': 45,
            },
            {
                'name': 'Cybersecurity Fundamentals',
                'code': 'SEC301',
                'description': 'Introduction to cybersecurity concepts, network security, and ethical hacking.',
                'credits': 3,
                'category': 'elective',
                'prerequisites': 'Computer Networks, Operating Systems',
                'max_students': 30,
            },
            {
                'name': 'Data Structures and Algorithms',
                'code': 'DSA201',
                'description': 'Comprehensive study of data structures, algorithms, and their analysis.',
                'credits': 4,
                'category': 'core',
                'prerequisites': 'CS101',
                'max_students': 50,
            },
            {
                'name': 'Digital Marketing Analytics',
                'code': 'DMA201',
                'description': 'Learn digital marketing strategies and analytics tools for measuring campaign effectiveness.',
                'credits': 2,
                'category': 'optional',
                'prerequisites': 'Basic statistics knowledge',
                'max_students': 40,
            },
            {
                'name': 'Project Management',
                'code': 'PM301',
                'description': 'Study project management methodologies, tools, and best practices for successful project delivery.',
                'credits': 2,
                'category': 'optional',
                'prerequisites': 'None',
                'max_students': 60,
            },
        ]

        for module_data in modules_data:
            module, created = Module.objects.get_or_create(
                code=module_data['code'],
                defaults=module_data
            )
            if created:
                self.stdout.write(f'Created module: {module.code} - {module.name}')
            else:
                self.stdout.write(f'Module already exists: {module.code}')

    def create_sample_students(self):
        """Create sample students for testing."""
        sample_students = [
            {
                'username': 'john_doe',
                'email': 'john.doe@student.edu',
                'first_name': 'John',
                'last_name': 'Doe',
                'password': 'student123'
            },
            {
                'username': 'jane_smith',
                'email': 'jane.smith@student.edu',
                'first_name': 'Jane',
                'last_name': 'Smith',
                'password': 'student123'
            },
            {
                'username': 'mike_johnson',
                'email': 'mike.johnson@student.edu',
                'first_name': 'Mike',
                'last_name': 'Johnson',
                'password': 'student123'
            },
        ]

        for student_data in sample_students:
            if not User.objects.filter(username=student_data['username']).exists():
                user = User.objects.create_user(
                    username=student_data['username'],
                    email=student_data['email'],
                    first_name=student_data['first_name'],
                    last_name=student_data['last_name'],
                    password=student_data['password']
                )
                
                # Create student profile
                student = Student.objects.create(
                    user=user,
                    is_verified=True,  # Pre-verify for testing
                    phone='+1-555-0123',
                    address='123 Student Street',
                    city='Education City',
                    country='United States'
                )
                
                self.stdout.write(f'Created student: {user.username}')
            else:
                self.stdout.write(f'Student already exists: {student_data["username"]}')

    def create_sample_registrations(self):
        """Create sample registrations for testing."""
        students = Student.objects.filter(is_verified=True)
        modules = Module.objects.filter(status='active')
        
        if not students.exists() or not modules.exists():
            self.stdout.write(self.style.WARNING('No verified students or active modules found for registrations'))
            return
        
        # Create random registrations
        for student in students:
            # Each student registers for 2-4 random modules
            num_registrations = random.randint(2, 4)
            selected_modules = random.sample(list(modules), min(num_registrations, len(modules)))
            
            for module in selected_modules:
                # Check if registration already exists
                if not Registration.objects.filter(student=student, module=module).exists():
                    Registration.objects.create(
                        student=student,
                        module=module,
                        status='enrolled',
                        is_active=True
                    )
                    self.stdout.write(f'Registered {student.user.username} for {module.code}')
        
        self.stdout.write(self.style.SUCCESS('Sample registrations created!'))
