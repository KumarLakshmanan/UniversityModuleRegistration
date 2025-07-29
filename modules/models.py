from django.db import models
from django.utils.text import slugify


class Module(models.Model):
    CATEGORY_CHOICES = [
        ('CORE', 'Core'),
        ('ELECTIVE', 'Elective'), 
        ('OPTIONAL', 'Optional'),
        ('SPECIALIZED', 'Specialized'),
    ]
    
    SEMESTER_CHOICES = [
        ('fall_2024', 'Fall 2024'),
        ('spring_2025', 'Spring 2025'),
        ('summer_2025', 'Summer 2025'),
        ('fall_2025', 'Fall 2025'),
    ]
    
    name = models.CharField(max_length=200)
    code = models.SlugField(max_length=20, unique=True)
    description = models.TextField()
    credits = models.PositiveIntegerField(default=3)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='CORE')
    semester = models.CharField(max_length=20, choices=SEMESTER_CHOICES, default='fall_2024')
    prerequisites = models.ManyToManyField('self', blank=True, symmetrical=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.code} - {self.name}"
    
    def save(self, *args, **kwargs):
        if not self.code:
            self.code = slugify(self.name.replace(' ', '_'))[:20]
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'modules'
        verbose_name = 'Module'
        verbose_name_plural = 'Modules'
        ordering = ['code']
