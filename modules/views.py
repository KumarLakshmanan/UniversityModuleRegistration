from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Module, Registration
from students.models import Student


class ModuleListView(ListView):
    """Module list view with search and pagination"""
    model = Module
    template_name = 'modules/list.html'
    context_object_name = 'modules'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Module.objects.filter(availability=True)
        search_query = self.request.GET.get('search')
        
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(code__icontains=search_query) |
                Q(description__icontains=search_query)
            )
        
        return queryset.order_by('name')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        return context


class ModuleDetailView(DetailView):
    """Module detail view"""
    model = Module
    template_name = 'modules/detail.html'
    context_object_name = 'module'
    slug_field = 'code'
    slug_url_kwarg = 'code'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        module = self.get_object()
        
        # Get registered students
        context['registered_students'] = module.registrations.select_related('student__user').all()
        
        # Check if current user is registered
        if self.request.user.is_authenticated:
            try:
                student = self.request.user.student
                context['is_registered'] = module.registrations.filter(student=student).exists()
            except:
                context['is_registered'] = False
        else:
            context['is_registered'] = False
            
        return context


class ModuleRegistrationView(LoginRequiredMixin, View):
    """AJAX module registration view"""
    login_url = '/auth/login/'
    
    def post(self, request, code):
        try:
            # Check if user's email is verified
            if hasattr(request.user, 'student') and not request.user.student.is_email_verified:
                return JsonResponse({
                    'success': False,
                    'message': 'Please verify your email address before registering for modules.'
                })
                
            module = get_object_or_404(Module, code=code, availability=True)
            student = request.user.student
            
            # Check if already registered
            if Registration.objects.filter(student=student, module=module).exists():
                return JsonResponse({
                    'success': False,
                    'message': 'You are already registered for this module.'
                })
            
            # Check if module is full
            if module.is_full:
                return JsonResponse({
                    'success': False,
                    'message': 'This module is full.'
                })
            
            # Create registration
            Registration.objects.create(student=student, module=module)
            
            return JsonResponse({
                'success': True,
                'message': f'Successfully registered for {module.name}!'
            })
            
        except Student.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Student profile not found. Please complete your profile.'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': 'An error occurred. Please try again.'
            })


class ModuleUnregistrationView(LoginRequiredMixin, View):
    """AJAX module unregistration view"""
    login_url = '/auth/login/'
    
    def post(self, request, code):
        try:
            # Check if user's email is verified
            if hasattr(request.user, 'student') and not request.user.student.is_email_verified:
                return JsonResponse({
                    'success': False,
                    'message': 'Please verify your email address before managing module registrations.'
                })
                
            module = get_object_or_404(Module, code=code)
            student = request.user.student
            
            # Check if registered
            registration = Registration.objects.filter(student=student, module=module).first()
            if not registration:
                return JsonResponse({
                    'success': False,
                    'message': 'You are not registered for this module.'
                })
            
            # Delete registration
            registration.delete()
            
            return JsonResponse({
                'success': True,
                'message': f'Successfully unregistered from {module.name}!'
            })
            
        except Student.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Student profile not found.'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': 'An error occurred. Please try again.'
            })
