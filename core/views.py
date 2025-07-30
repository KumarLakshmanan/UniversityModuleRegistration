from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Count
from students.models import Student
from modules.models import Module, Registration
from .models import Contact
import requests


class HomeView(TemplateView):
    """Home page view"""
    template_name = 'core/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'total_modules': Module.objects.filter(availability=True).count(),
            'total_students': Student.objects.count(),
            'total_registrations': Registration.objects.count(),
            'featured_modules': Module.objects.filter(availability=True)[:3],
        })
        return context


class AboutView(TemplateView):
    """About page view"""
    template_name = 'core/about.html'


class ContactView(TemplateView):
    """Contact page view with form handling"""
    template_name = 'core/contact.html'
    
    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        if all([name, email, subject, message]):
            try:
                # Save to database
                contact = Contact.objects.create(
                    name=name,
                    email=email,
                    subject=subject,
                    message=message
                )
                
                # Send email (if email is configured)
                if settings.EMAIL_HOST_USER:
                    send_mail(
                        subject=f"Contact Form: {subject}",
                        message=f"From: {name} ({email})\n\n{message}",
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[settings.DEFAULT_FROM_EMAIL],
                        fail_silently=False,
                    )
                
                messages.success(request, 'Thank you for your message! We will get back to you soon.')
                return redirect('core:contact')
            except Exception as e:
                messages.error(request, 'There was an error sending your message. Please try again.')
        else:
            messages.error(request, 'Please fill in all required fields.')
        
        return render(request, self.template_name)


class UnauthorizedView(TemplateView):
    """Unauthorized access page"""
    template_name = 'core/unauthorized.html'
    
    def get(self, request, *args, **kwargs):
        messages.warning(request, 'You need to be logged in to access that page.')
        return super().get(request, *args, **kwargs)
