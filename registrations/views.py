from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from .models import Registration
from students.models import Student


class MyModulesView(LoginRequiredMixin, ListView):
    """
    View showing all modules the current student is registered for.
    """
    model = Registration
    template_name = 'registrations/my_modules.html'
    context_object_name = 'registrations'
    paginate_by = 10
    login_url = '/login/'
    
    def get_queryset(self):
        # Get or create student profile
        if not hasattr(self, '_student'):
            self._student, created = Student.objects.get_or_create(user=self.request.user)
        
        return Registration.objects.filter(
            student=self._student,
            is_active=True
        ).select_related('module__course').order_by('-date_registered')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Use the cached student
        if not hasattr(self, '_student'):
            self._student, created = Student.objects.get_or_create(user=self.request.user)
        
        context['student'] = self._student
        
        # Calculate total credits from the current queryset
        registrations = context['registrations']
        total_credits = sum(reg.module.credits for reg in registrations)
        context['total_credits'] = total_credits
        
        # Use a single query to get all status counts
        all_registrations = Registration.objects.filter(student=self._student)
        context['status_counts'] = {
            'enrolled': all_registrations.filter(status='enrolled', is_active=True).count(),
            'completed': all_registrations.filter(status='completed').count(),
            'withdrawn': all_registrations.filter(status='withdrawn').count(),
        }
        
        return context
