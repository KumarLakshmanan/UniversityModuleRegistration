from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.db.models import Q
from .models import Course, Module
from registrations.models import Registration
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST


class CourseListView(ListView):
    """
    Course list view with search and filtering capabilities.
    """
    model = Course
    template_name = 'modules/course_list.html'
    context_object_name = 'courses'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Course.objects.filter(status='active').order_by('course_code')
        
        # Search functionality
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(course_code__icontains=search_query) |
                Q(description__icontains=search_query)
            )
        
        # Filter by availability
        available_only = self.request.GET.get('available')
        if available_only:
            queryset = queryset.filter(is_available_for_registration=True)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        context['available_only'] = self.request.GET.get('available', '')
        
        return context


class CourseDetailView(DetailView):
    """
    Course detail view showing course information and modules.
    """
    model = Course
    template_name = 'modules/course_detail.html'
    context_object_name = 'course'
    slug_field = 'course_code'
    slug_url_kwarg = 'course_code'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = self.get_object()
        
        # Get modules in this course
        modules = Module.objects.filter(course=course, status='active').order_by('code')
        
        # Add registration status for each module if user is authenticated
        if self.request.user.is_authenticated:
            try:
                student = self.request.user.student_profile
                registered_module_ids = set(
                    Registration.objects.filter(
                        student=student, 
                        module__course=course,
                        is_active=True
                    ).values_list('module_id', flat=True)
                )
                
                for module in modules:
                    module.is_registered = module.id in registered_module_ids
                    module.can_register_check = module.can_register() and not module.is_registered
                    
            except Exception:
                for module in modules:
                    module.is_registered = False
                    module.can_register_check = module.can_register()
        else:
            for module in modules:
                module.is_registered = False
                module.can_register_check = module.can_register()
        
        context['modules'] = modules
        
        # Get enrolled students for this course (unique students across all modules)
        enrolled_students = Registration.objects.filter(
            module__course=course,
            is_active=True
        ).select_related('student__user', 'module').order_by('-date_registered')
        
        context['enrolled_students'] = enrolled_students
        context['enrolled_count'] = course.enrolled_students_count
        
        return context


# Keep the old module views for backward compatibility temporarily
class ModuleListView(ListView):
    """
    Redirect to CourseListView - for backward compatibility.
    """
    def get(self, request, *args, **kwargs):
        from django.shortcuts import redirect
        return redirect('modules:course_list')


class ModuleDetailView(DetailView):
    """
    Module detail view - now shows the course that contains this module.
    """
    model = Module
    template_name = 'modules/module_detail.html'
    context_object_name = 'module'
    slug_field = 'code'
    slug_url_kwarg = 'code'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        module = self.get_object()
        course = module.course
        
        # Get all modules in the same course
        course_modules = Module.objects.filter(course=course, status='active').order_by('code')
        context['course_modules'] = course_modules
        context['course'] = course
        
        # Check if current user is registered for this specific module
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


# Module registration views
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
