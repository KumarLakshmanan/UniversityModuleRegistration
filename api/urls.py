from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'api'

# Create a router and register our viewsets
router = DefaultRouter()
router.register(r'students', views.StudentViewSet)
router.register(r'modules', views.ModuleViewSet)
router.register(r'registrations', views.RegistrationViewSet)

urlpatterns = [
    # API root
    path('', views.api_root, name='api_root'),
    
    # API Documentation
    path('docs/', views.APIDocsView.as_view(), name='api_docs'),
    
    # ViewSet URLs
    path('', include(router.urls)),
    
    # Custom API endpoints
    path('auth/register/', views.RegisterAPIView.as_view(), name='auth_register'),
    path('auth/login/', views.LoginAPIView.as_view(), name='auth_login'),
    path('auth/logout/', views.LogoutAPIView.as_view(), name='auth_logout'),
    path('auth/verify-email/', views.VerifyEmailAPIView.as_view(), name='auth_verify_email'),
    path('auth/password-reset/', views.PasswordResetAPIView.as_view(), name='auth_password_reset'),
    path('auth/password-reset-confirm/', views.PasswordResetConfirmAPIView.as_view(), name='auth_password_reset_confirm'),
    
    # Module registration endpoints
    path('modules/<int:module_id>/register/', views.ModuleRegistrationAPIView.as_view(), name='module_register'),
    path('modules/<int:module_id>/unregister/', views.ModuleRegistrationAPIView.as_view(), name='module_unregister'),
    
    # Register for a module by code
    path('modules/<str:code>/register/', views.ModuleRegisterByCodeAPIView.as_view(), name='module_register'),
    # Unregister from a module by code
    path('modules/<str:code>/unregister/', views.ModuleUnregisterByCodeAPIView.as_view(), name='module_unregister'),

    # Other endpoints
    path('contact/', views.ContactAPIView.as_view(), name='contact'),
    path('stats/', views.SystemStatsAPIView.as_view(), name='stats'),
    path('profile/', views.UserProfileAPIView.as_view(), name='profile'),
    
    # System stats
    path('stats/', views.SystemStatsAPIView.as_view(), name='system_stats'),
    
    # Contact form
    path('contact/', views.ContactAPIView.as_view(), name='contact'),
]
