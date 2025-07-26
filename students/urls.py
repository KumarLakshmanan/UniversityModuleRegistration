from django.urls import path
from . import views

app_name = 'students'

urlpatterns = [
    path('register/', views.StudentRegistrationView.as_view(), name='register'),
    path('login/', views.StudentLoginView.as_view(), name='login'),
    path('logout/', views.StudentLogoutView.as_view(), name='logout'),
    path('verify-email/', views.EmailVerificationView.as_view(), name='verify_email'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/edit/', views.ProfileUpdateView.as_view(), name='profile_edit'),
    path('my-modules/', views.MyModulesView.as_view(), name='my_modules'),
    path('password-reset/', views.PasswordResetRequestView.as_view(), name='password_reset'),
    path('password-reset-verify/', views.PasswordResetVerifyView.as_view(), name='password_reset_verify'),
    path('password-reset-confirm/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]
