from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib import messages
from django.http import JsonResponse
from .models import SystemStats, ContactMessage
from students.models import Student
from modules.models import Module
from registrations.models import Registration


class HomeView(TemplateView):
    """
    Home page view displaying system statistics and hero section.
    """
    template_name = 'sitecore/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get or update system stats
        stats = SystemStats.get_latest_stats()
        stats.update_stats()
        
        context['stats'] = {
            'total_students': stats.total_students,
            'total_modules': stats.total_modules,
            'total_registrations': stats.total_registrations,
            'active_modules': stats.active_modules,
            'active_registrations': stats.active_registrations,
        }
        
        # Get recent modules for homepage
        context['featured_modules'] = Module.objects.filter(
            status='active',
            is_available_for_registration=True
        ).order_by('-created_at')[:3]
        
        return context


class AboutView(TemplateView):
    """
    About page view with static content about the institution.
    """
    template_name = 'sitecore/about.html'


class ContactView(TemplateView):
    """
    Contact page view with contact form.
    """
    template_name = 'sitecore/contact.html'
    
    def post(self, request, *args, **kwargs):
        """Handle contact form submission."""
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        subject = request.POST.get('subject', '').strip()
        message = request.POST.get('message', '').strip()
        phone = request.POST.get('phone', '').strip()
        
        # Validate required fields
        errors = {}
        if not name:
            errors['name'] = 'This field is required'
        if not email:
            errors['email'] = 'This field is required'
        elif '@' not in email:
            errors['email'] = 'Please enter a valid email address'
        if not subject:
            errors['subject'] = 'This field is required'
        if not message:
            errors['message'] = 'This field is required'
        
        # Handle AJAX requests
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            if errors:
                return JsonResponse({
                    'success': False,
                    'errors': errors
                }, status=400)
            
            try:
                # Create contact message
                contact_message = ContactMessage.objects.create(
                    name=name,
                    email=email,
                    subject=subject,
                    message=message,
                    phone=phone
                )
                
                return JsonResponse({
                    'success': True,
                    'message': 'Thank you for your message! We will get back to you soon.'
                })
                
            except Exception as e:
                return JsonResponse({
                    'success': False,
                    'message': 'Sorry, there was an error sending your message. Please try again.'
                }, status=500)
        
        # Handle regular form submission
        if errors:
            for field, error_msg in errors.items():
                messages.error(request, error_msg)
            return render(request, self.template_name)
        
        try:
            # Create contact message
            contact_message = ContactMessage.objects.create(
                name=name,
                email=email,
                subject=subject,
                message=message,
                phone=phone
            )
            
            messages.success(request, 'Thank you for your message! We will get back to you soon.')
            return redirect('sitecore:contact')
            
        except Exception as e:
            messages.error(request, 'Sorry, there was an error sending your message. Please try again.')
            return render(request, self.template_name)


class UnauthorizedView(TemplateView):
    """
    Unauthorized access warning page.
    """
    template_name = 'sitecore/unauthorized.html'
