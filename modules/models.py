from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Module(models.Model):
    """Module model for university modules"""
    
    CATEGORY_CHOICES = [
        ('core', 'Core'),
        ('elective', 'Elective'),
        ('optional', 'Optional'),
        ('prerequisite', 'Prerequisite'),
    ]
    
    name = models.CharField(max_length=200)
    code = models.SlugField(max_length=20, unique=True)
    credit = models.PositiveIntegerField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='core')
    description = models.TextField()
    availability = models.BooleanField(default=True)
    max_students = models.PositiveIntegerField(default=100, help_text="Maximum number of students")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.code} - {self.name}"

    def get_absolute_url(self):
        return reverse('modules:detail', kwargs={'code': self.code})

    @property
    def registered_students_count(self):
        """Get the number of registered students"""
        return self.registrations.count()

    @property
    def available_spots(self):
        """Get available spots remaining"""
        return self.max_students - self.registered_students_count

    @property
    def is_full(self):
        """Check if module is at capacity"""
        return self.registered_students_count >= self.max_students


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
