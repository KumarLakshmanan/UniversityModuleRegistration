from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.utils.timezone import now


class Student(models.Model):
    """
    Student profile model extending Django's User model.
    Contains additional fields specific to student information.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    
    # Personal Information
    date_of_birth = models.DateField(null=True, blank=True)
    phone = models.CharField(
        max_length=15, 
        blank=True, 
        validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be valid.")]
    )
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    
    # Profile Picture
    photo = models.ImageField(upload_to='student_photos/', blank=True, null=True)
    
    # Account Status
    is_verified = models.BooleanField(default=False)
    verification_token = models.CharField(max_length=255, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Student"
        verbose_name_plural = "Students"
        ordering = ['-created_at']

    def __str__(self):
        full_name = self.user.get_full_name()
        if full_name:
            return f"{self.user.username} - {full_name}"
        return self.user.username

    def get_full_name(self):
        """Return the full name of the student."""
        return self.user.get_full_name() or self.user.username

    @property
    def profile_picture(self):
        """Alias for photo field to match test expectations."""
        return self.photo
    
    @property
    def is_profile_complete(self):
        """Check if the student profile is complete."""
        required_fields = [
            self.user.first_name,
            self.user.last_name,
            self.user.email,
            self.date_of_birth,
            self.phone,
            self.address,
            self.city,
            self.country
        ]
        return all(field for field in required_fields)


class OTP(models.Model):
    """
    OTP model for email verification and password reset.
    """
    PURPOSE_CHOICES = [
        ('verification', 'Email Verification'),
        ('password_reset', 'Password Reset'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='otps')
    otp_code = models.CharField(max_length=6)
    purpose = models.CharField(max_length=20, choices=PURPOSE_CHOICES)
    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    class Meta:
        verbose_name = "OTP"
        verbose_name_plural = "OTPs"
        ordering = ['-created_at']

    def __str__(self):
        return f"OTP {self.otp_code} for {self.user.username} ({self.purpose})"

    @property
    def is_expired(self):
        """Check if the OTP has expired."""
        return now() > self.expires_at

    @property
    def is_valid(self):
        """Check if the OTP is valid (not used and not expired)."""
        return not self.is_used and not self.is_expired
