from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Course(models.Model):
    """Course model - one course can have multiple modules"""
    
    name = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('modules:course_detail', kwargs={'pk': self.pk})

    @property
    def total_credits(self):
        """Get total credits for all modules in this course"""
        return self.modules.aggregate(total=models.Sum('credit'))['total'] or 0

    @property
    def total_modules(self):
        """Get total number of modules in this course"""
        return self.modules.count()

    @property
    def registered_students_count(self):
        """Get total number of students registered across all modules in this course"""
        total_registrations = 0
        for module in self.modules.all():
            total_registrations += module.current_enrollment
        return total_registrations

    @property
    def total_capacity(self):
        """Get total capacity across all modules in this course"""
        return self.modules.aggregate(total=models.Sum('max_students'))['total'] or 0

    @property
    def available_spots(self):
        """Get total available spots across all modules in this course"""
        return max(0, self.total_capacity - self.registered_students_count)

    @property
    def is_full(self):
        """Check if all modules in this course are at capacity"""
        return self.available_spots == 0


class Module(models.Model):
    """Module model for university modules - belongs to a course"""
    
    CATEGORY_CHOICES = [
        ('core', 'Core'),
        ('elective', 'Elective'),
        ('optional', 'Optional'),
        ('prerequisite', 'Prerequisite'),
    ]
    
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules', null=True, blank=True)
    name = models.CharField(max_length=200)
    code = models.SlugField(max_length=20, unique=True)
    credit = models.PositiveIntegerField()
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='core')
    availability = models.BooleanField(default=True, help_text="Is this module available for registration?")
    max_students = models.PositiveIntegerField(default=50, help_text="Maximum number of students")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.code} - {self.name}"

    def get_absolute_url(self):
        return reverse('modules:module_detail', kwargs={'code': self.code})

    @property
    def current_enrollment(self):
        """Get current number of registered students"""
        return self.registrations.count()

    @property
    def available_spots(self):
        """Get number of available spots"""
        return max(0, self.max_students - self.current_enrollment)

    @property
    def is_full(self):
        """Check if module is at capacity"""
        return self.current_enrollment >= self.max_students

    def can_register(self, student):
        """Check if a student can register for this module"""
        if not self.availability:
            return False, "Module is not available for registration"
        
        if self.is_full:
            return False, "Module is full"
        
        # Check if already registered
        if self.registrations.filter(student=student).exists():
            return False, "Already registered for this module"
        
        return True, "Can register"


class Registration(models.Model):
    """Registration model linking students to modules"""
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE, related_name='registrations')
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='registrations')
    date_registered = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'module')
        ordering = ['-date_registered']

    def __str__(self):
        return f"{self.student.user.username} - {self.module.code}"
