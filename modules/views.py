from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse

from .models import Module
from registrations.models import Registration
from students.models import Student


def module_list_view(request):
    """Public view of all active modules"""
    modules = Module.objects.filter(is_active=True)
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        modules = modules.filter(
            Q(name__icontains=search_query) |
            Q(code__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    # Filter by credits
    credits = request.GET.get('credits')
    if credits:
        modules = modules.filter(credits=credits)
    
    # Pagination
    paginator = Paginator(modules, 12)  # Show 12 modules per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get filter options
    credit_options = Module.objects.filter(is_active=True).values_list('credits', flat=True).distinct()
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'credits': credits,
        'credit_options': sorted(set(credit_options)),
    }
    return render(request, 'modules/module_list.html', context)


def module_detail_view(request, module_id):
    """Detailed view of a module"""
    module = get_object_or_404(Module, id=module_id, is_active=True)
    
    # Check if user is authenticated and registered for this module
    is_registered = False
    registration = None
    student = None
    
    if request.user.is_authenticated:
        try:
            student = Student.objects.get(user=request.user)
            registration = Registration.objects.filter(student=student, module=module).first()
            is_registered = registration is not None
        except Student.DoesNotExist:
            pass
    
    # Get registration statistics
    total_registrations = Registration.objects.filter(module=module).count()
    enrolled_students = Registration.objects.filter(module=module, status='enrolled').count()
    
    context = {
        'module': module,
        'is_registered': is_registered,
        'registration': registration,
        'student': student,
        'stats': {
            'total_registrations': total_registrations,
            'enrolled_students': enrolled_students,
        }
    }
    return render(request, 'modules/module_detail.html', context)


@login_required
def module_search_view(request):
    """AJAX search for modules"""
    query = request.GET.get('q', '')
    modules = Module.objects.filter(is_active=True)
    
    if query:
        modules = modules.filter(
            Q(name__icontains=query) |
            Q(code__icontains=query) |
            Q(description__icontains=query)
        )[:10]  # Limit to 10 results
    
    results = []
    for module in modules:
        results.append({
            'id': module.id,
            'code': module.code,
            'name': module.name,
            'credits': module.credits,
        })
    
    return JsonResponse({'results': results})

