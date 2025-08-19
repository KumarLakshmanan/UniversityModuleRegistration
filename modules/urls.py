from django.urls import path
from . import views

app_name = 'modules'

urlpatterns = [
    # Course URLs (main functionality)
    path('', views.CourseListView.as_view(), name='list'),  # Course list page
    path('courses/<int:pk>/', views.CourseDetailView.as_view(), name='course_detail'),
    
    # Module registration URLs (used within course detail)
    path('modules/<slug:code>/register/', views.ModuleRegistrationView.as_view(), name='module_register'),
    path('modules/<slug:code>/unregister/', views.ModuleUnregistrationView.as_view(), name='module_unregister'),
    
    # Legacy module URLs (for backward compatibility)
    path('modules/', views.ModuleListView.as_view(), name='module_list'),
    path('modules/<slug:code>/', views.ModuleDetailView.as_view(), name='module_detail'),
    
    # Keep old URLs for backward compatibility (redirect to courses)
    path('<int:pk>/', views.CourseDetailView.as_view(), name='detail'),
]
