from django.urls import path
from . import views

app_name = 'students'

urlpatterns = [
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('profile/setup/', views.profile_setup_view, name='profile_setup'),
    path('profile/edit/', views.profile_edit_view, name='profile_edit'),
    path('student/modules/', views.modules_view, name='modules'),
    path('registrations/', views.registrations_view, name='registrations'),
    path('register/<int:module_id>/', views.register_module_view, name='register_module'),
    path('unregister/<int:module_id>/', views.unregister_module_view, name='unregister_module'),
]
