from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from modules.models import Module, Registration
from students.models import Student
from datetime import date
import random


class Command(BaseCommand):
    help = 'Populate the database with sample data'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Creating sample data...'))

        # Create sample modules
        modules_data = [
            {
                'name': 'Introduction to Computer Science',
                'code': 'CS101',
                'credit': 3,
                'category': 'core',
                'description': 'Fundamental concepts of computer science including programming basics, algorithms, and data structures.',
                'max_students': 30
            },
            {
                'name': 'Database Management Systems',
                'code': 'CS201',
                'credit': 4,
                'category': 'core',
                'description': 'Comprehensive study of database design, SQL, normalization, and database administration.',
                'max_students': 25
            },
            {
                'name': 'Web Development',
                'code': 'CS301',
                'credit': 3,
                'category': 'elective',
                'description': 'Modern web development techniques using HTML, CSS, JavaScript, and popular frameworks.',
                'max_students': 20
            },
            {
                'name': 'Data Analytics',
                'code': 'DA101',
                'credit': 3,
                'category': 'elective',
                'description': 'Introduction to data analysis, statistical methods, and data visualization techniques.',
                'max_students': 25
            },
            {
                'name': 'Machine Learning',
                'code': 'ML201',
                'credit': 4,
                'category': 'elective',
                'description': 'Fundamentals of machine learning algorithms, supervised and unsupervised learning.',
                'max_students': 20
            },
            {
                'name': 'Software Engineering',
                'code': 'SE301',
                'credit': 3,
                'category': 'core',
                'description': 'Software development lifecycle, design patterns, testing, and project management.',
                'max_students': 30
            },
            {
                'name': 'Mobile App Development',
                'code': 'MAD201',
                'credit': 3,
                'category': 'elective',
                'description': 'Development of mobile applications for iOS and Android platforms.',
                'max_students': 15
            },
            {
                'name': 'Cybersecurity Fundamentals',
                'code': 'CYB101',
                'credit': 3,
                'category': 'optional',
                'description': 'Introduction to cybersecurity concepts, threats, and protection mechanisms.',
                'max_students': 25
            },
            {
                'name': 'Digital Marketing',
                'code': 'MKT201',
                'credit': 2,
                'category': 'optional',
                'description': 'Digital marketing strategies, social media marketing, and online advertising.',
                'max_students': 30
            },
            {
                'name': 'Project Management',
                'code': 'PM101',
                'credit': 2,
                'category': 'optional',
                'description': 'Project planning, execution, monitoring, and risk management principles.',
                'max_students': 35
            }
        ]

        # Create modules
        for module_data in modules_data:
            module, created = Module.objects.get_or_create(
                code=module_data['code'],
                defaults=module_data
            )
            if created:
                self.stdout.write(f'Created module: {module.name}')

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

        # Create some sample registrations
        students = Student.objects.all()
        modules = Module.objects.all()
        
        for student in students:
            # Register each student for 2-4 random modules
            num_modules = random.randint(2, 4)
            selected_modules = random.sample(list(modules), num_modules)
            
            for module in selected_modules:
                Registration.objects.get_or_create(
                    student=student,
                    module=module
                )
            
            self.stdout.write(f'Created registrations for: {student.user.get_full_name()}')

        self.stdout.write(
            self.style.SUCCESS('Successfully populated database with sample data!')
        )
