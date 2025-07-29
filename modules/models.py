from django.db import models
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator


class Module(models.Model):
    """
    Course Module model representing academic courses/modules
    that students can register for.
    """
    CATEGORY_CHOICES = [
        ('core', 'Core Module'),
        ('elective', 'Elective Module'),
        ('optional', 'Optional Module'),
        ('foundation', 'Foundation Module'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('archived', 'Archived'),
    ]
    
    # Basic Information
    name = models.CharField(max_length=200)
    code = models.SlugField(max_length=20, unique=True, help_text="Module code (e.g., CS101)")
    description = models.TextField()
    
    # Academic Details
    credits = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(20)],
        help_text="Number of credits for this module"
    )
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='core')
    prerequisites = models.TextField(blank=True, help_text="Prerequisites for this module")
    
    # Status and Availability
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    is_available_for_registration = models.BooleanField(default=True)
    max_students = models.PositiveIntegerField(
        null=True, 
        blank=True, 
        help_text="Maximum number of students allowed (leave blank for unlimited)"
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Module"
        verbose_name_plural = "Modules"
        ordering = ['code']

    def __str__(self):
        return f"{self.code} - {self.name}"

    def save(self, *args, **kwargs):
        """Auto-generate slug from code if not provided."""
        if not self.code:
            self.code = slugify(self.name)[:20]
        super().save(*args, **kwargs)

    @property
    def enrolled_students_count(self):
        """Return the number of students enrolled in this module."""
        return self.registrations.filter(is_active=True).count()

    @property
    def available_spots(self):
        """Return the number of available spots for registration."""
        if not self.max_students:
            return None  # Unlimited
        return max(0, self.max_students - self.enrolled_students_count)

    @property
    def is_full(self):
        """Check if the module has reached its maximum capacity."""
        if not self.max_students:
            return False
        return self.enrolled_students_count >= self.max_students

    def can_register(self):
        """Check if new students can register for this module."""
        return (
            self.status == 'active' and 
            self.is_available_for_registration and 
            not self.is_full
        )
