from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from students.models import Student
from modules.models import Module


class Registration(models.Model):
    """
    Registration model tracking student enrollment in modules.
    """
    STATUS_CHOICES = [
        ('enrolled', 'Enrolled'),
        ('completed', 'Completed'),
        ('withdrawn', 'Withdrawn'),
        ('failed', 'Failed'),
    ]
    
    # Relationships
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='registrations')
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='registrations')
    
    # Registration Details
    date_registered = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='enrolled')
    is_active = models.BooleanField(default=True)
    
    # Academic Information
    grade = models.CharField(max_length=5, blank=True, null=True, help_text="Final grade (A, B, C, D, F)")
    completion_date = models.DateTimeField(null=True, blank=True)
    
    # Withdrawal Information
    withdrawal_date = models.DateTimeField(null=True, blank=True)
    withdrawal_reason = models.TextField(blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Registration"
        verbose_name_plural = "Registrations"
        ordering = ['-date_registered']
        # Ensure a student can only register once for a module
        unique_together = ('student', 'module')

    def __str__(self):
        return f"{self.student.get_full_name()} - {self.module.code}"

    def withdraw(self, reason=""):
        """Withdraw the student from the module."""
        self.status = 'withdrawn'
        self.is_active = False
        self.withdrawal_date = timezone.now()
        self.withdrawal_reason = reason
        self.save()

    def complete(self, grade=""):
        """Mark the registration as completed."""
        self.status = 'completed'
        self.is_active = False
        self.completion_date = timezone.now()
        self.grade = grade
        self.save()

    @property
    def duration_enrolled(self):
        """Calculate how long the student has been enrolled."""
        end_date = self.completion_date or self.withdrawal_date or timezone.now()
        return end_date - self.date_registered

    @property
    def can_withdraw(self):
        """Check if the student can withdraw from this module."""
        return self.is_active and self.status == 'enrolled'
