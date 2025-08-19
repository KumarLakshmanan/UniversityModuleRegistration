from django.urls import path
from . import views

app_name = 'modules'

urlpatterns = [
    # Course browsing (new primary routes)
    path('courses/', views.CourseListView.as_view(), name='course_list'),
    path('courses/<slug:course_code>/', views.CourseDetailView.as_view(), name='course_detail'),
    
    # Module browsing
    path('', views.ModuleListView.as_view(), name='list'),
    path('<slug:code>/', views.ModuleDetailView.as_view(), name='detail'),
    path('modules/<slug:code>/', views.ModuleDetailView.as_view(), name='module_detail'),
    
    # Module registration actions (AJAX)
    path('<int:pk>/register/', views.module_register, name='register'),
    path('<int:pk>/unregister/', views.module_unregister, name='unregister'),
]
