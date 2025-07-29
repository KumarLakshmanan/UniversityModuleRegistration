from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect

from .models import Student
from modules.models import Module
from registrations.models import Registration
from portalcontent.models import SiteConfiguration


@login_required
def dashboard_view(request):
    """Student dashboard view"""
    try:
        student = Student.objects.get(user=request.user)
    except Student.DoesNotExist:
        # If no student profile exists, redirect to create one
        messages.warning(request, 'Please complete your student profile.')
        return redirect('students:profile_setup')
    
    # Get student's registrations
    registrations = Registration.objects.filter(student=student).select_related('module')
    
    # Get available modules for registration
    site_config = SiteConfiguration.objects.first()
    available_modules = Module.objects.filter(is_active=True)
    
    # Calculate stats
    total_credits = sum(reg.module.credits for reg in registrations.filter(status__in=['enrolled', 'completed']))
    pending_registrations = registrations.filter(status='pending').count()
    completed_modules = registrations.filter(status='completed').count()
    
    context = {
        'student': student,
        'registrations': registrations,
        'available_modules': available_modules[:5],  # Show only first 5
        'site_config': site_config,
        'stats': {
            'total_credits': total_credits,
            'pending_registrations': pending_registrations,
            'completed_modules': completed_modules,
            'total_registrations': registrations.count(),
        }
    }
    return render(request, 'students/dashboard.html', context)


@login_required
@csrf_protect
def profile_setup_view(request):
    """Student profile setup view"""
    try:
        student = Student.objects.get(user=request.user)
        # If profile exists, redirect to profile edit
        return redirect('students:profile_edit')
    except Student.DoesNotExist:
        pass
    
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        phone_number = request.POST.get('phone_number')
        date_of_birth = request.POST.get('date_of_birth')
        address = request.POST.get('address')
        profile_picture = request.FILES.get('profile_picture')
        
        # Validation
        if not all([student_id, phone_number, date_of_birth, address]):
            messages.error(request, 'All fields except profile picture are required.')
            return render(request, 'students/profile_setup.html')
        
        # Check if student ID is unique
        if Student.objects.filter(student_id=student_id).exists():
            messages.error(request, 'Student ID already exists.')
            return render(request, 'students/profile_setup.html')
        
        try:
            student = Student.objects.create(
                user=request.user,
                student_id=student_id,
                phone_number=phone_number,
                date_of_birth=date_of_birth,
                address=address,
                profile_picture=profile_picture
            )
            messages.success(request, 'Profile created successfully!')
            return redirect('students:dashboard')
        except Exception as e:
            messages.error(request, 'Failed to create profile. Please try again.')
    
    return render(request, 'students/profile_setup.html')


@login_required
@csrf_protect
def profile_edit_view(request):
    """Student profile edit view"""
    try:
        student = Student.objects.get(user=request.user)
    except Student.DoesNotExist:
        return redirect('students:profile_setup')
    
    if request.method == 'POST':
        student.phone_number = request.POST.get('phone_number', student.phone_number)
        student.address = request.POST.get('address', student.address)
        
        if request.FILES.get('profile_picture'):
            student.profile_picture = request.FILES['profile_picture']
        
        try:
            student.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('students:dashboard')
        except Exception as e:
            messages.error(request, 'Failed to update profile. Please try again.')
    
    context = {'student': student}
    return render(request, 'students/profile_edit.html', context)


@login_required
def modules_view(request):
    """View available modules"""
    try:
        student = Student.objects.get(user=request.user)
    except Student.DoesNotExist:
        return redirect('students:profile_setup')
    
    # Get all active modules
    modules = Module.objects.filter(is_active=True)
    
    # Filter by semester if specified
    semester = request.GET.get('semester')
    if semester:
        modules = modules.filter(semester=semester)
    
    # Get student's current registrations
    student_registrations = Registration.objects.filter(student=student).values_list('module_id', flat=True)
    
    # Add registration status to modules
    for module in modules:
        module.is_registered = module.id in student_registrations
    
    # Get unique semesters for filter
    semesters = Module.objects.filter(is_active=True).values_list('semester', flat=True).distinct()
    
    context = {
        'student': student,
        'modules': modules,
        'semesters': sorted(set(semesters)),
        'current_semester': semester
    }
    return render(request, 'students/modules.html', context)


@login_required
def registrations_view(request):
    """View student's module registrations"""
    try:
        student = Student.objects.get(user=request.user)
    except Student.DoesNotExist:
        return redirect('students:profile_setup')
    
    registrations = Registration.objects.filter(student=student).select_related('module').order_by('-registration_date')
    
    # Filter by status if specified
    status_filter = request.GET.get('status')
    if status_filter:
        registrations = registrations.filter(status=status_filter)
    
    context = {
        'student': student,
        'registrations': registrations,
        'status_filter': status_filter,
        'status_choices': Registration.STATUS_CHOICES
    }
    return render(request, 'students/registrations.html', context)


@login_required
@csrf_protect
def register_module_view(request, module_id):
    """Register for a module"""
    try:
        student = Student.objects.get(user=request.user)
    except Student.DoesNotExist:
        messages.error(request, 'Please complete your student profile first.')
        return redirect('students:profile_setup')
    
    module = get_object_or_404(Module, id=module_id, is_active=True)
    
    # Check if already registered
    if Registration.objects.filter(student=student, module=module).exists():
        messages.warning(request, f'You are already registered for {module.name}.')
        return redirect('students:modules')
    
    # Check site configuration
    site_config = SiteConfiguration.objects.first()
    if site_config and not site_config.is_registration_open:
        messages.error(request, 'Module registration is currently closed.')
        return redirect('students:modules')
    
    if request.method == 'POST':
        try:
            Registration.objects.create(
                student=student,
                module=module,
                status='pending'
            )
            messages.success(request, f'Successfully registered for {module.name}!')
        except Exception as e:
            messages.error(request, 'Registration failed. Please try again.')
    
    return redirect('students:modules')


@login_required
@csrf_protect
def unregister_module_view(request, module_id):
    """Unregister from a module"""
    try:
        student = Student.objects.get(user=request.user)
    except Student.DoesNotExist:
        messages.error(request, 'Student profile not found.')
        return redirect('students:profile_setup')
    
    module = get_object_or_404(Module, id=module_id)
    
    try:
        registration = Registration.objects.get(student=student, module=module)
        
        # Only allow unregistration for pending/enrolled status
        if registration.status in ['pending', 'enrolled']:
            registration.delete()
            messages.success(request, f'Successfully unregistered from {module.name}.')
        else:
            messages.error(request, f'Cannot unregister from {module.name}. Status: {registration.get_status_display()}')
    except Registration.DoesNotExist:
        messages.error(request, 'You are not registered for this module.')
    
    return redirect('students:registrations')
