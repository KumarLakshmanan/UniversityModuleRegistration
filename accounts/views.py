from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from django.http import JsonResponse
import random
import string

from .models import OTPVerification
from students.models import Student


def generate_otp():
    """Generate a 6-digit OTP"""
    return ''.join(random.choices(string.digits, k=6))


@csrf_protect
def register_view(request):
    """User registration view"""
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        
        # Validation
        if not all([username, email, first_name, last_name, password, password_confirm]):
            messages.error(request, 'All fields are required.')
            return render(request, 'accounts/register.html')
        
        if password != password_confirm:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'accounts/register.html')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return render(request, 'accounts/register.html')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return render(request, 'accounts/register.html')
        
        # Create user
        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name,
                password=password
            )
            user.is_active = False  # User needs to verify email
            user.save()
            
            # Generate and send OTP
            otp_code = generate_otp()
            OTPVerification.objects.create(
                user=user,
                otp_code=otp_code,
                expires_at=timezone.now() + timezone.timedelta(minutes=15)
            )
            
            # In a real application, send email here
            # For now, we'll just show a message
            messages.success(request, f'Registration successful! Please verify your email with OTP: {otp_code}')
            return redirect('accounts:verify_otp', user_id=user.id)
            
        except Exception as e:
            messages.error(request, 'Registration failed. Please try again.')
            return render(request, 'accounts/register.html')
    
    return render(request, 'accounts/register.html')


@csrf_protect
def login_view(request):
    """User login view"""
    if request.user.is_authenticated:
        return redirect('students:dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if not username or not password:
            messages.error(request, 'Username and password are required.')
            return render(request, 'accounts/login.html')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                next_url = request.GET.get('next', 'students:dashboard')
                return redirect(next_url)
            else:
                messages.error(request, 'Account is not verified. Please verify your email.')
                return redirect('accounts:verify_otp', user_id=user.id)
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'accounts/login.html')


def logout_view(request):
    """User logout view"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('portalcontent:home')


def verify_otp_view(request, user_id):
    """Verify OTP for email verification"""
    try:
        user = User.objects.get(id=user_id)
        otp_verification = OTPVerification.objects.filter(
            user=user, 
            is_used=False,
            expires_at__gt=timezone.now()
        ).first()
        
        if not otp_verification:
            messages.error(request, 'OTP expired or invalid.')
            return redirect('accounts:register')
        
        if request.method == 'POST':
            otp_code = request.POST.get('otp_code')
            
            if otp_code == otp_verification.otp_code:
                otp_verification.is_used = True
                otp_verification.save()
                
                user.is_active = True
                user.save()
                
                messages.success(request, 'Email verified successfully! You can now login.')
                return redirect('accounts:login')
            else:
                messages.error(request, 'Invalid OTP code.')
        
        context = {
            'user': user,
            'otp_verification': otp_verification
        }
        return render(request, 'accounts/verify_otp.html', context)
        
    except User.DoesNotExist:
        messages.error(request, 'Invalid user.')
        return redirect('accounts:register')


def resend_otp_view(request, user_id):
    """Resend OTP for email verification"""
    try:
        user = User.objects.get(id=user_id)
        
        # Invalidate old OTPs
        OTPVerification.objects.filter(user=user, is_used=False).delete()
        
        # Generate new OTP
        otp_code = generate_otp()
        OTPVerification.objects.create(
            user=user,
            otp_code=otp_code,
            expires_at=timezone.now() + timezone.timedelta(minutes=15)
        )
        
        messages.success(request, f'New OTP sent: {otp_code}')
        return redirect('accounts:verify_otp', user_id=user.id)
        
    except User.DoesNotExist:
        messages.error(request, 'Invalid user.')
        return redirect('accounts:register')


@login_required
def profile_view(request):
    """User profile view"""
    try:
        student = Student.objects.get(user=request.user)
    except Student.DoesNotExist:
        student = None
    
    context = {
        'student': student
    }
    return render(request, 'accounts/profile.html', context)


def admin_login_blocked(request):
    """Block admin login via /auth/login/ - redirect to unauthorized page"""
    messages.warning(request, 'Admin login via this URL is not allowed. Please use the admin panel directly.')
    return redirect('portalcontent:unauthorized')
