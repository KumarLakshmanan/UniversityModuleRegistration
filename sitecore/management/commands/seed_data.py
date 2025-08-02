from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from students.models import Student
from modules.models import Module
from registrations.models import Registration
from sitecore.models import SystemStats, ContactMessage
import random


class Command(BaseCommand):
    help = 'Seed the database with initial data'

    def handle(self, *args, **options):
        self.stdout.write('Seeding database with initial data...')
        
        # Set admin password
        admin = User.objects.get(username='admin')
        admin.set_password('Admin!2025')
        admin.save()
        self.stdout.write('Admin password set')

        # Create sample students
        students_data = [
            {'username': 'john_doe', 'email': 'john@example.com', 'first_name': 'John', 'last_name': 'Doe'},
            {'username': 'jane_smith', 'email': 'jane@example.com', 'first_name': 'Jane', 'last_name': 'Smith'},
            {'username': 'mike_johnson', 'email': 'mike@example.com', 'first_name': 'Mike', 'last_name': 'Johnson'},
            {'username': 'sarah_wilson', 'email': 'sarah@example.com', 'first_name': 'Sarah', 'last_name': 'Wilson'},
            {'username': 'david_brown', 'email': 'david@example.com', 'first_name': 'David', 'last_name': 'Brown'},
        ]

        for student_data in students_data:
            if not User.objects.filter(username=student_data['username']).exists():
                user = User.objects.create_user(
                    username=student_data['username'],
                    email=student_data['email'],
                    first_name=student_data['first_name'],
                    last_name=student_data['last_name'],
                    password='student123'
                )
                Student.objects.create(
                    user=user,
                    phone=f"+1{random.randint(1000000000, 9999999999)}",
                    date_of_birth="1995-01-01",
                    is_verified=True
                )
                self.stdout.write(f'Created student: {student_data["username"]}')

        # Create sample modules
        modules_data = [
            {
                'code': 'CS101',
                'name': 'Introduction to Computer Science',
                'description': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris.',
                'credits': 3,
                'category': 'core',
                'max_students': 30,
                'image_url': 'https://images.unsplash.com/photo-1517077304055-6e89abbf09b0?w=800&h=600&fit=crop'
            },
            {
                'code': 'MATH201',
                'name': 'Advanced Mathematics',
                'description': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Mauris viverra venerat.',
                'credits': 4,
                'category': 'core',
                'max_students': 25,
                'image_url': 'https://images.unsplash.com/photo-1509228468518-180dd4864904?w=800&h=600&fit=crop'
            },
            {
                'code': 'ENG101',
                'name': 'English Literature',
                'description': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec auctor blandit quam, et molestie dolor tempus at. Nulla facilisi. Sed vel ex nec nulla tincidunt.',
                'credits': 3,
                'category': 'elective',
                'max_students': 20,
                'image_url': 'https://images.unsplash.com/photo-1481627834876-b7833e8f5570?w=800&h=600&fit=crop'
            },
            {
                'code': 'PHYS101',
                'name': 'General Physics',
                'description': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Cras in nisi id turpis cursus vulputate. Aliquam erat volutpat. Integer posuere erat a ante venenatis dapibus.',
                'credits': 4,
                'category': 'core',
                'max_students': 28,
                'image_url': 'https://images.unsplash.com/photo-1636466497217-26a8cbeaf0aa?w=800&h=600&fit=crop'
            },
            {
                'code': 'ART201',
                'name': 'Digital Art & Design',
                'description': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas.',
                'credits': 3,
                'category': 'elective',
                'max_students': 15,
                'image_url': 'https://images.unsplash.com/photo-1561998338-13ad7883b20f?w=800&h=600&fit=crop'
            },
            {
                'code': 'BIO101',
                'name': 'Introduction to Biology',
                'description': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed cursus ante dapibus diam. Sed nisi. Nulla quis sem at nibh elementum imperdiet.',
                'credits': 4,
                'category': 'core',
                'max_students': 22,
                'image_url': 'https://images.unsplash.com/photo-1559757148-5c350d0d3c56?w=800&h=600&fit=crop'
            }
        ]

        for module_data in modules_data:
            if not Module.objects.filter(code=module_data['code']).exists():
                Module.objects.create(**module_data)
                self.stdout.write(f'Created module: {module_data["code"]}')

        # Create sample registrations
        students = Student.objects.all()
        modules = Module.objects.all()
        
        statuses = ['enrolled', 'completed', 'withdrawn']
        for student in students[:3]:  # First 3 students
            for module in modules[:3]:  # First 3 modules
                if not Registration.objects.filter(student=student, module=module).exists():
                    Registration.objects.create(
                        student=student,
                        module=module,
                        status=random.choice(statuses),
                        grade=random.choice(['A', 'B', 'C', None])
                    )

        # Create sample contact messages
        contact_messages = [
            {
                'name': 'Alex Thompson',
                'email': 'alex@example.com',
                'subject': 'Registration Question',
                'message': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.'
            },
            {
                'name': 'Maria Garcia',
                'email': 'maria@example.com',
                'subject': 'Technical Support',
                'message': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Ut enim ad minim veniam, quis nostrud exercitation ullamco.'
            }
        ]

        for msg_data in contact_messages:
            ContactMessage.objects.create(**msg_data)

        # Create system stats
        if not SystemStats.objects.exists():
            SystemStats.objects.create()

        self.stdout.write(
            self.style.SUCCESS('Successfully seeded database with initial data!')
        )
