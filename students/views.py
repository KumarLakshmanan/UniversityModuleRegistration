from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.generic import TemplateView
from django.http import JsonResponse
from .models import Student
from registrations.models import Registration
from modules.models import Module


class DashboardView(LoginRequiredMixin, TemplateView):
    """
    Student dashboard view showing overview of registrations and profile.
    """
    template_name = 'students/dashboard.html'
    login_url = '/login/'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get or create student profile
        student, created = Student.objects.get_or_create(user=self.request.user)
        
        # Get student registrations
        registrations = Registration.objects.filter(
            student=student,
            is_active=True
        ).select_related('module').order_by('-date_registered')
        
        # Get registered modules
        registered_modules = [reg.module for reg in registrations]
        
        # Calculate total credits
        total_credits = sum(module.credits for module in registered_modules)
        
        # Get available modules (modules not registered for)
        from modules.models import Module
        registered_module_ids = [module.id for module in registered_modules]
        available_modules = Module.objects.filter(
            status='active',
            is_available_for_registration=True
        ).exclude(id__in=registered_module_ids)
        
        # Calculate stats
        enrolled_count = registrations.filter(status='enrolled').count()
        completed_count = Registration.objects.filter(student=student, status='completed').count()
        total_count = Registration.objects.filter(student=student).count()
        
        stats = {
            'enrolled': enrolled_count,
            'completed': completed_count,
            'total': total_count,
        }
        
        context.update({
            'student': student,
            'total_registrations': registrations.count(),
            'recent_registrations': registrations[:5],
            'profile_complete': student.is_profile_complete,
            'registered_modules': registered_modules,
            'total_credits': total_credits,
            'available_modules': available_modules,
            'stats': stats,
        })
        
        return context


class ProfileView(LoginRequiredMixin, TemplateView):
    """
    Student profile view for viewing profile information.
    """
    template_name = 'students/profile.html'
    login_url = '/login/'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get or create student profile
        student, created = Student.objects.get_or_create(user=self.request.user)
        context['student'] = student
        
        # Add completed registrations count
        context['completed_count'] = student.registrations.filter(status='completed').count()
        
        return context


class ProfileEditView(LoginRequiredMixin, TemplateView):
    """
    Student profile edit view for updating profile information.
    """
    template_name = 'students/profile_edit.html'
    login_url = '/login/'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get or create student profile
        student, created = Student.objects.get_or_create(user=self.request.user)
        context['student'] = student
        
        return context
    
    def post(self, request, *args, **kwargs):
        """Handle profile update form submission."""
        # Validate required fields
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip()
        
        errors = []
        
        # Required field validation
        if not first_name:
            errors.append('This field is required')
        if not last_name:
            errors.append('This field is required')
        if not email:
            errors.append('This field is required')
        elif '@' not in email:
            errors.append('Please enter a valid email address')
        
        # Check email uniqueness (exclude current user)
        if email and User.objects.filter(email=email).exclude(id=request.user.id).exists():
            errors.append('A user with this email already exists')
        
        if errors:
            for error in errors:
                messages.error(request, error)
            return self.get(request, *args, **kwargs)
        
        try:
            student = get_object_or_404(Student, user=request.user)
            
            # Update user fields
            request.user.first_name = first_name
            request.user.last_name = last_name
            request.user.email = email
            request.user.save()
            
            # Update student fields
            student.date_of_birth = request.POST.get('date_of_birth') or None
            student.phone = request.POST.get('phone', '')
            student.address = request.POST.get('address', '')
            student.city = request.POST.get('city', '')
            student.country = request.POST.get('country', '')
            
            # Handle photo upload
            if 'photo' in request.FILES:
                student.photo = request.FILES['photo']
            elif 'profile_picture' in request.FILES:
                student.photo = request.FILES['profile_picture']
            
            student.save()
            
            messages.success(request, 'Profile updated successfully!')
            return redirect('students:profile')
            
        except Exception as e:
            messages.error(request, 'Error updating profile. Please try again.')
            return self.get(request, *args, **kwargs)
