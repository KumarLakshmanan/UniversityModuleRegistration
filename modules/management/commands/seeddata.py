from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from modules.models import Module
from students.models import Student
from registrations.models import Registration
from portalcontent.models import SiteConfiguration, NewsUpdate
from accounts.models import ContactMessage
import random


class Command(BaseCommand):
    help = 'Load initial seed data for the university system'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting to load seed data...'))
        
        # Create site configuration
        self.create_site_config()
        
        # Create sample modules
        self.create_modules()
        
        # Create sample users and students
        self.create_users_and_students()
        
        # Create sample registrations
        self.create_registrations()
        
        # Create sample news updates
        self.create_news_updates()
        
        # Create sample contact messages
        self.create_contact_messages()
        
        self.stdout.write(self.style.SUCCESS('Successfully loaded seed data!'))

    def create_site_config(self):
        """Create site configuration if it doesn't exist"""
        if not SiteConfiguration.objects.exists():
            config = SiteConfiguration.objects.create(
                site_name="University Module Registration System",
                site_description="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
                contact_email="info@university.edu",
                contact_phone="+1-555-123-4567",
                address="123 University Ave, Academic City, State 12345",
                about_content="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.",
                is_active=True
            )
            self.stdout.write(f'Created site configuration: {config.site_name}')

    def create_modules(self):
        """Create sample modules"""
        modules_data = [
            {
                'code': 'CS101',
                'name': 'Introduction to Computer Science',
                'description': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.',
                'image_url': 'https://images.unsplash.com/photo-1481627834876-b7833e8f5570?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80',
                'credits': 3,
                'category': 'CORE'
            },
            {
                'code': 'CS201',
                'name': 'Data Structures and Algorithms',
                'description': 'Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.',
                'image_url': 'https://images.unsplash.com/photo-1434030216411-0b793f4b4173?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80',
                'credits': 4,
                'category': 'CORE'
            },
            {
                'code': 'CS301',
                'name': 'Database Systems',
                'description': 'Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.',
                'image_url': 'https://images.unsplash.com/photo-1460925895917-afdab827c52f?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80',
                'credits': 3,
                'category': 'SPECIALIZED',
            },
            {
                'code': 'MATH101',
                'name': 'Calculus I',
                'description': 'Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
                'image_url': 'https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80',
                'credits': 4,
                'category': 'CORE',
            },
            {
                'code': 'MATH201',
                'name': 'Linear Algebra',
                'description': 'Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium.',
                'image_url': 'https://images.unsplash.com/photo-1635070041078-e363dbe005cb?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80',
                'credits': 3,
                'category': 'CORE',
            },
            {
                'code': 'ENG101',
                'name': 'Academic Writing',
                'description': 'Totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt.',
                'image_url': 'https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80',
                'credits': 3,
                'category': 'CORE',
            },
            {
                'code': 'PHYS101',
                'name': 'Physics I',
                'description': 'Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit.',
                'image_url': 'https://images.unsplash.com/photo-1636466497217-26a8cbeaf0aa?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80',
                'credits': 4,
                'category': 'ELECTIVE',
            },
            {
                'code': 'CS401',
                'name': 'Machine Learning',
                'description': 'Sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt.',
                'image_url': 'https://images.unsplash.com/photo-1677442136019-21780ecad995?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80',
                'credits': 3,
                'category': 'SPECIALIZED',
            },
        ]
        
        for module_data in modules_data:
            module, created = Module.objects.get_or_create(
                code=module_data['code'],
                defaults=module_data
            )
            if created:
                self.stdout.write(f'Created module: {module.code} - {module.name}')

    def create_users_and_students(self):
        """Create sample users and students"""
        students_data = [
            {
                'username': 'john_doe',
                'email': 'john.doe@student.university.edu',
                'first_name': 'John',
                'last_name': 'Doe',
                'password': 'student123',
                'phone_number': '+1-555-001-0001',
                'address': '123 Student St, Campus City, State 12345'
            },
            {
                'username': 'jane_smith',
                'email': 'jane.smith@student.university.edu',
                'first_name': 'Jane',
                'last_name': 'Smith',
                'password': 'student123',
                'phone_number': '+1-555-001-0002',
                'address': '456 University Ave, Campus City, State 12345'
            },
            {
                'username': 'mike_johnson',
                'email': 'mike.johnson@student.university.edu',
                'first_name': 'Mike',
                'last_name': 'Johnson',
                'password': 'student123',
                'phone_number': '+1-555-001-0003',
                'address': '789 Academic Blvd, Campus City, State 12345'
            },
            {
                'username': 'sarah_wilson',
                'email': 'sarah.wilson@student.university.edu',
                'first_name': 'Sarah',
                'last_name': 'Wilson',
                'password': 'student123',
                'phone_number': '+1-555-001-0004',
                'address': '321 Scholar Lane, Campus City, State 12345'
            },
        ]
        
        for student_data in students_data:
            user, created = User.objects.get_or_create(
                username=student_data['username'],
                defaults={
                    'email': student_data['email'],
                    'first_name': student_data['first_name'],
                    'last_name': student_data['last_name'],
                    'is_active': True
                }
            )
            if created:
                user.set_password(student_data['password'])
                user.save()
                self.stdout.write(f'Created user: {user.username}')
            
            student, created = Student.objects.get_or_create(
                user=user,
                defaults={
                    'phone_number': student_data['phone_number'],
                    'address': student_data['address']
                }
            )
            if created:
                self.stdout.write(f'Created student: {student.student_id}')

    def create_registrations(self):
        """Create sample registrations"""
        students = Student.objects.all()
        modules = Module.objects.all()
        statuses = ['enrolled', 'completed', 'pending']
        
        # Create random registrations
        for student in students:
            # Each student registers for 2-4 random modules
            num_registrations = random.randint(2, 4)
            selected_modules = random.sample(list(modules), min(num_registrations, len(modules)))
            
            for module in selected_modules:
                registration, created = Registration.objects.get_or_create(
                    student=student,
                    module=module,
                    defaults={
                        'status': random.choice(statuses),
                        'grade': random.choice(['A', 'B', 'C', 'D', '']) if random.choice([True, False]) else ''
                    }
                )
                if created:
                    self.stdout.write(f'Created registration: {student.user.username} -> {module.code}')

    def create_news_updates(self):
        """Create sample news updates"""
        news_data = [
            {
                'title': 'Welcome to Fall 2024 Semester',
                'content': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris.',
                'is_published': True
            },
            {
                'title': 'New Computer Science Modules Added',
                'content': 'Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim.',
                'is_published': True
            },
            {
                'title': 'Campus Library Extended Hours',
                'content': 'Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis.',
                'is_published': True
            },
            {
                'title': 'Spring 2025 Registration Opens Soon',
                'content': 'Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt.',
                'is_published': False
            },
        ]
        
        for news_item in news_data:
            news, created = NewsUpdate.objects.get_or_create(
                title=news_item['title'],
                defaults=news_item
            )
            if created:
                self.stdout.write(f'Created news update: {news.title}')

    def create_contact_messages(self):
        """Create sample contact messages"""
        messages_data = [
            {
                'name': 'Alex Thompson',
                'email': 'alex.thompson@email.com',
                'subject': 'Question about module prerequisites',
                'message': 'I would like to know more about the prerequisites for the Advanced Database Systems module. Could you please provide more information?',
                'is_read': False
            },
            {
                'name': 'Emily Chen',
                'email': 'emily.chen@email.com',
                'subject': 'Registration deadline inquiry',
                'message': 'What is the deadline for module registration for the current semester? I want to make sure I don\'t miss it.',
                'is_read': True
            },
            {
                'name': 'David Rodriguez',
                'email': 'david.rodriguez@email.com',
                'subject': 'Technical support needed',
                'message': 'I am having trouble accessing my student dashboard. Could someone help me resolve this issue?',
                'is_read': False
            },
        ]
        
        for message_data in messages_data:
            message, created = ContactMessage.objects.get_or_create(
                email=message_data['email'],
                subject=message_data['subject'],
                defaults=message_data
            )
            if created:
                self.stdout.write(f'Created contact message: {message.subject}')
