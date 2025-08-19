from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from modules.models import Course, Module, Registration
from students.models import Student
from datetime import date
import random


class Command(BaseCommand):
    help = 'Populate the database with sample data for courses and modules'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Creating sample data...'))

        # Create sample courses
        courses_data = [
            {
                'name': 'Computer Science Fundamentals',
                'description': 'Introduction to computer science concepts including programming, algorithms, and data structures.'
            },
            {
                'name': 'Advanced Database Systems',
                'description': 'Comprehensive study of advanced database design, optimization, and distributed systems.'
            },
            {
                'name': 'Full-Stack Web Development',
                'description': 'Complete web development course covering frontend, backend, and deployment.'
            },
            {
                'name': 'Data Science and Analytics',
                'description': 'Data analysis, machine learning, and statistical methods for data science.'
            },
            {
                'name': 'Digital Marketing Mastery',
                'description': 'Comprehensive digital marketing strategies and social media management.'
            },
            {
                'name': 'Cybersecurity Essentials',
                'description': 'Essential cybersecurity concepts and practical security implementations.'
            }
        ]

        # Create courses
        for course_data in courses_data:
            course, created = Course.objects.get_or_create(
                name=course_data['name'],
                defaults=course_data
            )
            if created:
                self.stdout.write(f'Created course: {course.name}')

        # Create sample modules for each course
        modules_data = {
            'Computer Science Fundamentals': [
                {'name': 'Introduction to Programming', 'code': 'CS101', 'credit': 4, 'category': 'core', 'description': 'Basic programming concepts using Python.'},
                {'name': 'Data Structures', 'code': 'CS102', 'credit': 3, 'category': 'core', 'description': 'Arrays, linked lists, stacks, and queues.'},
                {'name': 'Algorithms', 'code': 'CS103', 'credit': 3, 'category': 'core', 'description': 'Sorting, searching, and basic algorithm analysis.'}
            ],
            'Advanced Database Systems': [
                {'name': 'Database Design', 'code': 'CS201', 'credit': 4, 'category': 'core', 'description': 'Advanced database modeling and normalization.'},
                {'name': 'SQL Optimization', 'code': 'CS202', 'credit': 3, 'category': 'core', 'description': 'Query optimization and performance tuning.'},
                {'name': 'NoSQL Systems', 'code': 'CS203', 'credit': 3, 'category': 'elective', 'description': 'MongoDB, Redis, and distributed databases.'}
            ],
            'Full-Stack Web Development': [
                {'name': 'Frontend Development', 'code': 'WEB301', 'credit': 4, 'category': 'elective', 'description': 'React, Vue.js, and modern JavaScript frameworks.'},
                {'name': 'Backend APIs', 'code': 'WEB302', 'credit': 4, 'category': 'elective', 'description': 'RESTful APIs, GraphQL, and server development.'},
                {'name': 'DevOps and Deployment', 'code': 'WEB303', 'credit': 2, 'category': 'optional', 'description': 'CI/CD, Docker, and cloud deployment.'}
            ],
            'Data Science and Analytics': [
                {'name': 'Statistical Analysis', 'code': 'DS401', 'credit': 3, 'category': 'core', 'description': 'Statistical methods and data analysis techniques.'},
                {'name': 'Machine Learning', 'code': 'DS402', 'credit': 4, 'category': 'elective', 'description': 'Supervised and unsupervised learning algorithms.'},
                {'name': 'Data Visualization', 'code': 'DS403', 'credit': 3, 'category': 'elective', 'description': 'Creating effective visualizations and dashboards.'}
            ],
            'Digital Marketing Mastery': [
                {'name': 'Social Media Marketing', 'code': 'MKT501', 'credit': 3, 'category': 'elective', 'description': 'Social media strategies and content creation.'},
                {'name': 'SEO and SEM', 'code': 'MKT502', 'credit': 3, 'category': 'elective', 'description': 'Search engine optimization and marketing.'},
                {'name': 'Analytics and ROI', 'code': 'MKT503', 'credit': 2, 'category': 'optional', 'description': 'Marketing analytics and return on investment.'}
            ],
            'Cybersecurity Essentials': [
                {'name': 'Network Security', 'code': 'CYB601', 'credit': 4, 'category': 'core', 'description': 'Network protocols and security implementations.'},
                {'name': 'Ethical Hacking', 'code': 'CYB602', 'credit': 3, 'category': 'elective', 'description': 'Penetration testing and vulnerability assessment.'},
                {'name': 'Security Policies', 'code': 'CYB603', 'credit': 3, 'category': 'prerequisite', 'description': 'Security governance and compliance frameworks.'}
            ]
        }

        # Create modules for each course
        for course_name, modules in modules_data.items():
            try:
                course = Course.objects.get(name=course_name)
                for module_data in modules:
                    module, created = Module.objects.get_or_create(
                        code=module_data['code'],
                        defaults={
                            'name': module_data['name'],
                            'description': module_data['description'],
                            'credit': module_data['credit'],
                            'course': course,
                            'max_students': 30,  # Default capacity
                            'availability': True,
                            'category': module_data['category']
                        }
                    )
                    if created:
                        self.stdout.write(f'Created module: {module.name} for course {course.name}')
            except Course.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'Course {course_name} not found'))

        # Create sample students
        students_data = [
            {
                'username': 'john_doe',
                'email': 'john.doe@student.university.edu',
                'first_name': 'John',
                'last_name': 'Doe',
                'date_of_birth': date(2000, 5, 15),
                'address': '123 Student Street',
                'city': 'Boston',
                'country': 'USA'
            },
            {
                'username': 'jane_smith',
                'email': 'jane.smith@student.university.edu',
                'first_name': 'Jane',
                'last_name': 'Smith',
                'date_of_birth': date(1999, 8, 22),
                'address': '456 Campus Ave',
                'city': 'Cambridge',
                'country': 'USA'
            },
            {
                'username': 'bob_wilson',
                'email': 'bob.wilson@student.university.edu',
                'first_name': 'Bob',
                'last_name': 'Wilson',
                'date_of_birth': date(2001, 3, 10),
                'address': '789 University Blvd',
                'city': 'New York',
                'country': 'USA'
            },
            {
                'username': 'alice_brown',
                'email': 'alice.brown@student.university.edu',
                'first_name': 'Alice',
                'last_name': 'Brown',
                'date_of_birth': date(2000, 11, 5),
                'address': '321 Education Lane',
                'city': 'San Francisco',
                'country': 'USA'
            },
            {
                'username': 'charlie_davis',
                'email': 'charlie.davis@student.university.edu',
                'first_name': 'Charlie',
                'last_name': 'Davis',
                'date_of_birth': date(1998, 12, 18),
                'address': '654 Learning St',
                'city': 'Seattle',
                'country': 'USA'
            }
        ]

        # Create users and students
        for student_data in students_data:
            user_data = {
                'username': student_data['username'],
                'email': student_data['email'],
                'first_name': student_data['first_name'],
                'last_name': student_data['last_name']
            }
            
            user, created = User.objects.get_or_create(
                username=user_data['username'],
                defaults=user_data
            )
            
            if created:
                user.set_password('password123')  # Default password
                user.save()
                
                # Create student profile
                Student.objects.create(
                    user=user,
                    date_of_birth=student_data['date_of_birth'],
                    address=student_data['address'],
                    city=student_data['city'],
                    country=student_data['country'],
                    is_email_verified=True
                )
                
                self.stdout.write(f'Created student: {user.get_full_name()}')

        # Create module registrations
        students = Student.objects.all()
        modules = Module.objects.all()
        
        for student in students:
            # Register each student for 2-5 random modules
            num_modules = random.randint(2, 5)
            selected_modules = random.sample(list(modules), min(num_modules, len(modules)))
            
            for module in selected_modules:
                Registration.objects.get_or_create(
                    student=student,
                    module=module
                )
            
            self.stdout.write(f'Created module registrations for: {student.user.get_full_name()}')

        self.stdout.write(
            self.style.SUCCESS('Successfully populated database with sample courses, modules, and registrations!')
        )
