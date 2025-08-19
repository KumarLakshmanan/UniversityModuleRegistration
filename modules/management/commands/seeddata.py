from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from modules.models import Course, Module
from students.models import Student
from registrations.models import Registration
import random


class Command(BaseCommand):
    help = 'Seed the database with sample data for development and testing'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting data seeding...'))
        
        # Create admin user if not exists
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'Admin!2025')
            self.stdout.write('Admin user created')
        else:
            # Set admin password
            admin = User.objects.get(username='admin')
            admin.set_password('Admin!2025')
            admin.save()
            self.stdout.write('Admin password set')

        # Create sample courses and modules
        self.create_sample_courses()
        
        # Create sample students (if needed)
        self.create_sample_students()
        
        # Create sample registrations
        self.create_sample_registrations()
        
        self.stdout.write(self.style.SUCCESS('Data seeding completed successfully!'))

    def create_sample_courses(self):
        """Create sample courses with their modules."""
        courses_data = [
            {
                'title': 'Computer Science Foundation',
                'course_code': 'CS-FOUND',
                'description': 'A comprehensive foundation course covering basic computer science concepts, programming fundamentals, and mathematical foundations.',
                'modules': [
                    {
                        'name': 'Introduction to Programming',
                        'code': 'PROG101',
                        'description': 'Learn programming fundamentals using Python, including variables, control structures, functions, and basic data structures.',
                        'credits': 4,
                        'category': 'core',
                        'prerequisites': 'None',
                    },
                    {
                        'name': 'Computer Mathematics',
                        'code': 'MATH101',
                        'description': 'Mathematical foundations for computer science including discrete mathematics, logic, and set theory.',
                        'credits': 3,
                        'category': 'core',
                        'prerequisites': 'High school mathematics',
                    },
                    {
                        'name': 'Computer Systems Basics',
                        'code': 'SYS101',
                        'description': 'Introduction to computer hardware, operating systems, and basic networking concepts.',
                        'credits': 3,
                        'category': 'core',
                        'prerequisites': 'None',
                    },
                ]
            },
            {
                'title': 'Web Development Complete',
                'course_code': 'WEB-DEV',
                'description': 'Complete web development course covering frontend, backend, and database technologies for modern web applications.',
                'modules': [
                    {
                        'name': 'Frontend Development',
                        'code': 'FRONT201',
                        'description': 'Learn HTML, CSS, JavaScript, and modern frontend frameworks like React for building user interfaces.',
                        'credits': 4,
                        'category': 'core',
                        'prerequisites': 'Basic programming knowledge',
                    },
                    {
                        'name': 'Backend Development',
                        'code': 'BACK201',
                        'description': 'Server-side programming with Node.js/Django, API development, and server management.',
                        'credits': 4,
                        'category': 'core',
                        'prerequisites': 'Programming fundamentals',
                    },
                    {
                        'name': 'Database Management',
                        'code': 'DB201',
                        'description': 'Database design, SQL, NoSQL databases, and database optimization techniques.',
                        'credits': 3,
                        'category': 'core',
                        'prerequisites': 'Basic programming knowledge',
                    },
                    {
                        'name': 'Web Security',
                        'code': 'SEC201',
                        'description': 'Web application security, authentication, authorization, and common vulnerabilities.',
                        'credits': 3,
                        'category': 'elective',
                        'prerequisites': 'Frontend and Backend Development',
                    },
                ]
            },
            {
                'title': 'Data Science & Analytics',
                'course_code': 'DATA-SCI',
                'description': 'Comprehensive data science course covering statistics, machine learning, data visualization, and big data technologies.',
                'modules': [
                    {
                        'name': 'Statistics for Data Science',
                        'code': 'STAT301',
                        'description': 'Statistical concepts, probability, hypothesis testing, and statistical inference for data analysis.',
                        'credits': 4,
                        'category': 'core',
                        'prerequisites': 'Mathematics foundations',
                    },
                    {
                        'name': 'Machine Learning Fundamentals',
                        'code': 'ML301',
                        'description': 'Introduction to machine learning algorithms, supervised and unsupervised learning, model evaluation.',
                        'credits': 5,
                        'category': 'core',
                        'prerequisites': 'Statistics and Programming',
                    },
                    {
                        'name': 'Data Visualization',
                        'code': 'VIZ301',
                        'description': 'Data visualization techniques using tools like Matplotlib, Plotly, and D3.js for effective data communication.',
                        'credits': 3,
                        'category': 'core',
                        'prerequisites': 'Programming fundamentals',
                    },
                    {
                        'name': 'Big Data Technologies',
                        'code': 'BIG301',
                        'description': 'Working with large datasets using Hadoop, Spark, and cloud-based big data platforms.',
                        'credits': 4,
                        'category': 'elective',
                        'prerequisites': 'Database management and programming',
                    },
                ]
            },
            {
                'title': 'Mobile App Development',
                'course_code': 'MOBILE-DEV',
                'description': 'Complete mobile application development course for iOS and Android platforms using modern frameworks.',
                'modules': [
                    {
                        'name': 'Mobile UI/UX Design',
                        'code': 'UI401',
                        'description': 'Mobile user interface design principles, user experience best practices, and prototyping tools.',
                        'credits': 3,
                        'category': 'core',
                        'prerequisites': 'Basic design knowledge',
                    },
                    {
                        'name': 'React Native Development',
                        'code': 'RN401',
                        'description': 'Cross-platform mobile app development using React Native framework for iOS and Android.',
                        'credits': 4,
                        'category': 'core',
                        'prerequisites': 'JavaScript and React knowledge',
                    },
                    {
                        'name': 'Native iOS Development',
                        'code': 'IOS401',
                        'description': 'Native iOS app development using Swift, Xcode, and iOS SDK frameworks.',
                        'credits': 4,
                        'category': 'elective',
                        'prerequisites': 'Programming fundamentals',
                    },
                    {
                        'name': 'Native Android Development',
                        'code': 'AND401',
                        'description': 'Native Android app development using Kotlin, Android Studio, and Android SDK.',
                        'credits': 4,
                        'category': 'elective',
                        'prerequisites': 'Programming fundamentals',
                    },
                ]
            },
            {
                'title': 'Cybersecurity Specialization',
                'course_code': 'CYBER-SEC',
                'description': 'Comprehensive cybersecurity course covering network security, ethical hacking, and security management.',
                'modules': [
                    {
                        'name': 'Network Security',
                        'code': 'NET501',
                        'description': 'Network security fundamentals, firewalls, VPNs, intrusion detection, and network monitoring.',
                        'credits': 4,
                        'category': 'core',
                        'prerequisites': 'Networking fundamentals',
                    },
                    {
                        'name': 'Ethical Hacking',
                        'code': 'HACK501',
                        'description': 'Penetration testing, vulnerability assessment, and ethical hacking methodologies.',
                        'credits': 4,
                        'category': 'core',
                        'prerequisites': 'Network security basics',
                    },
                    {
                        'name': 'Cryptography',
                        'code': 'CRYPT501',
                        'description': 'Cryptographic algorithms, digital signatures, PKI, and cryptographic protocols.',
                        'credits': 3,
                        'category': 'core',
                        'prerequisites': 'Mathematics and programming',
                    },
                    {
                        'name': 'Security Management',
                        'code': 'MGMT501',
                        'description': 'Information security governance, risk management, compliance, and security policies.',
                        'credits': 3,
                        'category': 'elective',
                        'prerequisites': 'Basic security concepts',
                    },
                ]
            },
            {
                'title': 'Digital Marketing Analytics',
                'course_code': 'DIGITAL-MKT',
                'description': 'Digital marketing course focusing on analytics, social media marketing, and online advertising strategies.',
                'modules': [
                    {
                        'name': 'Digital Marketing Fundamentals',
                        'code': 'MKT201',
                        'description': 'Introduction to digital marketing, SEO, SEM, content marketing, and digital marketing strategies.',
                        'credits': 3,
                        'category': 'core',
                        'prerequisites': 'Basic business knowledge',
                    },
                    {
                        'name': 'Social Media Marketing',
                        'code': 'SMM201',
                        'description': 'Social media platforms, content creation, community management, and social media advertising.',
                        'credits': 3,
                        'category': 'core',
                        'prerequisites': 'Digital marketing fundamentals',
                    },
                    {
                        'name': 'Marketing Analytics',
                        'code': 'ANALYTICS201',
                        'description': 'Google Analytics, marketing metrics, A/B testing, and data-driven marketing decisions.',
                        'credits': 4,
                        'category': 'core',
                        'prerequisites': 'Basic statistics',
                    },
                ]
            },
        ]

        for course_data in courses_data:
            modules_data = course_data.pop('modules')
            course, created = Course.objects.get_or_create(
                course_code=course_data['course_code'],
                defaults=course_data
            )
            if created:
                self.stdout.write(f'Created course: {course.course_code} - {course.title}')
            else:
                self.stdout.write(f'Course already exists: {course.course_code}')
            
            # Create modules for this course
            for module_data in modules_data:
                module_data['course'] = course
                module, created = Module.objects.get_or_create(
                    course=course,
                    code=module_data['code'],
                    defaults=module_data
                )
                if created:
                    self.stdout.write(f'  Created module: {module.full_code} - {module.name}')
                else:
                    self.stdout.write(f'  Module already exists: {module.full_code}')

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
            {
                'username': 'sarah_williams',
                'email': 'sarah.williams@student.edu',
                'first_name': 'Sarah',
                'last_name': 'Williams',
                'password': 'student123'
            },
            {
                'username': 'david_brown',
                'email': 'david.brown@student.edu',
                'first_name': 'David',
                'last_name': 'Brown',
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
                    self.stdout.write(f'Registered {student.user.username} for {module.full_code}')
        
        self.stdout.write(self.style.SUCCESS('Sample registrations created!'))
