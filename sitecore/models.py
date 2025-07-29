from django.db import models
from django.core.validators import EmailValidator


class ContactMessage(models.Model):
    """
    Contact form submission model for storing messages
    sent through the contact page.
    """
    # Contact Information
    name = models.CharField(max_length=100)
    email = models.EmailField(validators=[EmailValidator()])
    subject = models.CharField(max_length=200)
    message = models.TextField()
    
    # Additional Information
    phone = models.CharField(max_length=20, blank=True)
    
    # Status
    is_read = models.BooleanField(default=False)
    is_replied = models.BooleanField(default=False)
    is_resolved = models.BooleanField(default=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Contact Message"
        verbose_name_plural = "Contact Messages"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.subject}"

    def mark_as_read(self):
        """Mark the message as read."""
        self.is_read = True
        self.save()

    def mark_as_replied(self):
        """Mark the message as replied."""
        self.is_replied = True
        self.save()


class SystemStats(models.Model):
    """
    Model to store system statistics displayed on the homepage.
    This could be automatically updated or manually managed.
    """
    total_students = models.PositiveIntegerField(default=0)
    total_modules = models.PositiveIntegerField(default=0)
    total_registrations = models.PositiveIntegerField(default=0)
    active_modules = models.PositiveIntegerField(default=0)
    
    # Timestamps
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "System Statistics"
        verbose_name_plural = "System Statistics"

    def __str__(self):
        return f"System Stats - Last Updated: {self.last_updated}"

    @classmethod
    def get_latest_stats(cls):
        """Get the latest system statistics."""
        stats, created = cls.objects.get_or_create(pk=1)
        return stats

    def update_stats(self):
        """Update statistics from the database."""
        from students.models import Student
        from modules.models import Module
        from registrations.models import Registration
        
        self.total_students = Student.objects.filter(is_verified=True).count()
        self.total_modules = Module.objects.filter(status='active').count()
        self.total_registrations = Registration.objects.filter(is_active=True).count()
        self.active_modules = Module.objects.filter(
            status='active', 
            is_available_for_registration=True
        ).count()
        self.save()
