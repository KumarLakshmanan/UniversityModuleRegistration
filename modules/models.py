from django.db import models
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator


class Course(models.Model):
    """
    Course model representing academic courses that contain multiple modules.
    """
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('archived', 'Archived'),
    ]
    
    # Basic Information
    title = models.CharField(max_length=200)
    course_code = models.SlugField(max_length=20, unique=True, help_text="Course code (e.g., CS-PROG)")
    description = models.TextField()
    
    # Status and Availability
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    is_available_for_registration = models.BooleanField(default=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Course"
        verbose_name_plural = "Courses"
        ordering = ['course_code']

    def __str__(self):
        return f"{self.course_code} - {self.title}"

    def save(self, *args, **kwargs):
        """Auto-generate slug from title if not provided."""
        if not self.course_code:
            self.course_code = slugify(self.title)[:20]
        super().save(*args, **kwargs)

    @property
    def total_credits(self):
        """Return the total credits for all modules in this course."""
        return self.modules.filter(status='active').aggregate(
            total=models.Sum('credits')
        )['total'] or 0

    @property
    def module_count(self):
        """Return the number of active modules in this course."""
        return self.modules.filter(status='active').count()

    @property
    def enrolled_students_count(self):
        """Return the number of unique students enrolled in modules of this course."""
        from registrations.models import Registration
        return Registration.objects.filter(
            module__course=self,
            is_active=True
        ).values('student').distinct().count()

    def can_register(self):
        """Check if new students can register for modules in this course."""
        return (
            self.status == 'active' and 
            self.is_available_for_registration and
            self.modules.filter(status='active').exists()
        )


class Module(models.Model):
    """
    Course Module model representing academic modules within courses.
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
    
    # Course relationship
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules')
    
    # Basic Information
    name = models.CharField(max_length=200)
    code = models.SlugField(max_length=20, help_text="Module code (e.g., CS101)")
    description = models.TextField()
    image_url = models.URLField(blank=True, null=True, help_text="URL for module image")
    
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
        # Ensure module code is unique within a course
        unique_together = ('course', 'code')

    def __str__(self):
        return f"{self.course.course_code}-{self.code} - {self.name}"

    def save(self, *args, **kwargs):
        """Auto-generate slug from name if not provided."""
        if not self.code:
            self.code = slugify(self.name)[:20]
        super().save(*args, **kwargs)

    @property
    def enrolled_students_count(self):
        """Return the number of students enrolled in this module's course."""
        return self.course.enrolled_students_count

    @property
    def full_code(self):
        """Return the full module code including course code."""
        return f"{self.course.course_code}-{self.code}"

    def can_register(self):
        """Check if new students can register for this module."""
        # Check course-level availability
        if not (self.course.can_register() and self.status == 'active'):
            return False
        
        # Check module-specific constraints
        if not self.is_available_for_registration:
            return False
            
        # Check max_students limit if set
        if self.max_students:
            from registrations.models import Registration
            current_enrolled = Registration.objects.filter(
                module=self,
                is_active=True
            ).count()
            if current_enrolled >= self.max_students:
                return False
        
        return True
