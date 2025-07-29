from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.db.models import Q
from .models import Module
from registrations.models import Registration
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST


class ModuleListView(ListView):
    """
    Module list view with search and filtering capabilities.
    """
    model = Module
    template_name = 'modules/list.html'
    context_object_name = 'modules'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Module.objects.filter(status='active').order_by('code')
        
        # Search functionality
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(code__icontains=search_query) |
                Q(description__icontains=search_query)
            )
        
        # Filter by category
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category=category)
        
        # Filter by availability
        available_only = self.request.GET.get('available')
        if available_only:
            queryset = queryset.filter(is_available_for_registration=True)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        context['selected_category'] = self.request.GET.get('category', '')
        context['available_only'] = self.request.GET.get('available', '')
        context['category_choices'] = Module.CATEGORY_CHOICES
        return context


class ModuleDetailView(DetailView):
    """
    Module detail view showing module information and enrollment options.
    """
    model = Module
    template_name = 'modules/detail.html'
    context_object_name = 'module'
    slug_field = 'code'
    slug_url_kwarg = 'code'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        module = self.get_object()
        
        # Get enrolled students
        registrations = Registration.objects.filter(
            module=module,
            is_active=True
        ).select_related('student__user').order_by('-date_registered')
        
        context['enrolled_students'] = registrations
        context['enrolled_count'] = registrations.count()
        
        # Calculate enrollment percentage if max_students is set
        if module.max_students:
            context['enrollment_percentage'] = (context['enrolled_count'] / module.max_students) * 100
        else:
            context['enrollment_percentage'] = 0
        
        # Check if current user is registered
        if self.request.user.is_authenticated:
            try:
                student = self.request.user.student_profile
                context['user_registered'] = Registration.objects.filter(
                    student=student,
                    module=module,
                    is_active=True
                ).exists()
            except:
                context['user_registered'] = False
        else:
            context['user_registered'] = False
        
        return context


@login_required
@require_POST
def module_register(request, pk):
    """AJAX view to register for a module."""
    module = get_object_or_404(Module, pk=pk)
    
    try:
        student = request.user.student_profile
        
        # Check if already registered
        existing = Registration.objects.filter(
            student=student,
            module=module,
            is_active=True
        ).exists()
        
        if existing:
            return JsonResponse({
                'success': False, 
                'message': 'You are already registered for this module.'
            }, status=400)
        
        # Check if module can accept registrations
        if not module.can_register():
            return JsonResponse({
                'success': False, 
                'message': 'This module is not available for registration.'
            }, status=400)
        
        # Create registration
        registration = Registration.objects.create(
            student=student,
            module=module,
            status='enrolled'
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Successfully registered for module.'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': 'Registration failed. Please try again.'
        }, status=500)


@login_required
@require_POST
def module_unregister(request, pk):
    """AJAX view to unregister from a module."""
    module = get_object_or_404(Module, pk=pk)
    
    try:
        student = request.user.student_profile
        
        # Find active registration
        registration = get_object_or_404(
            Registration,
            student=student,
            module=module,
            is_active=True
        )
        
        # Deactivate registration
        registration.is_active = False
        registration.status = 'withdrawn'
        registration.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Successfully unregistered from module.'
        })
        
    except Registration.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'You are not registered for this module.'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': 'Unregistration failed. Please try again.'
        }, status=500)
