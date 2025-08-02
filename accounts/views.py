from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.generic import TemplateView, View
from django.utils import timezone
from django.conf import settings
from students.models import Student, OTP
import random
import string
from datetime import timedelta


class LoginView(TemplateView):
    """
    User login view.
    """
    template_name = 'accounts/login.html'
    
    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Check if user is verified
            if hasattr(user, 'student_profile') and not user.student_profile.is_verified:
                messages.info(request, 'Please verify your email to complete your account setup.')
                # Store user ID in session for verification
                request.session['unverified_user_id'] = user.id
                return redirect('accounts:verify_email')
            
            login(request, user)
            next_url = request.GET.get('next', '/dashboard/')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')
            return render(request, self.template_name)


class RegisterView(TemplateView):
    """
    User registration view.
    """
    template_name = 'accounts/register.html'
    
    def post(self, request, *args, **kwargs):
        try:
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            password_confirm = request.POST.get('password_confirm')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            
            # Validation
            if password != password_confirm:
                messages.error(request, 'Passwords do not match.')
                return render(request, self.template_name)
            
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists.')
                return render(request, self.template_name)
            
            if User.objects.filter(email=email).exists():
                messages.error(request, 'Email already exists.')
                return render(request, self.template_name)
            
            # Create user
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            
            # Create student profile
            student = Student.objects.create(user=user)
            
            # Generate and send verification OTP
            self.send_verification_otp(user)
            
            messages.success(request, 'Registration successful! Please check your email for verification instructions.')
            return redirect('accounts:verify_email')
            
        except Exception as e:
            messages.error(request, 'Registration failed. Please try again.')
            return render(request, self.template_name)
    
    def send_verification_otp(self, user):
        """Generate and send verification OTP."""
        from django.core.mail import send_mail
        from django.template.loader import render_to_string
        
        otp_code = ''.join(random.choices(string.digits, k=6))
        expires_at = timezone.now() + timedelta(minutes=settings.OTP_EXPIRY_MINUTES)
        
        OTP.objects.create(
            user=user,
            otp_code=otp_code,
            purpose='verification',
            expires_at=expires_at
        )
        
        # Send email
        try:
            subject = 'Email Verification - Course Registration System'
            html_message = render_to_string('accounts/emails/otp_email.html', {
                'user': user,
                'otp_code': otp_code,
                'expiry_minutes': settings.OTP_EXPIRY_MINUTES
            })
            plain_message = f"Your verification code is: {otp_code}. This code expires in {settings.OTP_EXPIRY_MINUTES} minutes."
            
            send_mail(
                subject=subject,
                message=plain_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                html_message=html_message,
                fail_silently=False,
            )
            print(f"Verification OTP for {user.email}: {otp_code}")
        except Exception as e:
            print(f"Failed to send verification email: {e}")
            # Still print OTP for development
            print(f"Verification OTP for {user.email}: {otp_code}")


class LogoutView(View):
    """
    User logout view.
    """
    def get(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, 'You have been logged out successfully.')
        return redirect('sitecore:home')


class VerifyEmailView(TemplateView):
    """
    Email verification view.
    """
    template_name = 'accounts/verify_email.html'
    
    def post(self, request, *args, **kwargs):
        otp_code = request.POST.get('otp_code')
        email = request.POST.get('email')
        
        try:
            user = User.objects.get(email=email)
            otp = OTP.objects.filter(
                user=user,
                otp_code=otp_code,
                purpose='verification',
                is_used=False
            ).first()
            
            if otp and otp.is_valid:
                # Verify the user
                student = user.student_profile
                student.is_verified = True
                student.save()
                
                # Mark OTP as used
                otp.is_used = True
                otp.save()
                
                messages.success(request, 'Email verified successfully! You can now log in.')
                return redirect('accounts:login')
            else:
                messages.error(request, 'Invalid or expired OTP.')
                return render(request, self.template_name)
                
        except User.DoesNotExist:
            messages.error(request, 'User not found.')
            return render(request, self.template_name)


class ResendVerificationView(View):
    """
    Resend verification OTP.
    """
    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        
        try:
            user = User.objects.get(email=email)
            if user.student_profile.is_verified:
                messages.info(request, 'Your email is already verified.')
                return redirect('accounts:login')
            
            # Generate new OTP
            otp_code = ''.join(random.choices(string.digits, k=6))
            expires_at = timezone.now() + timedelta(minutes=settings.OTP_EXPIRY_MINUTES)
            
            OTP.objects.create(
                user=user,
                otp_code=otp_code,
                purpose='verification',
                expires_at=expires_at
            )
            
            # Send email
            try:
                from django.core.mail import send_mail
                from django.template.loader import render_to_string
                
                subject = 'Email Verification - Course Registration System'
                html_message = render_to_string('accounts/emails/otp_email.html', {
                    'user': user,
                    'otp_code': otp_code,
                    'expiry_minutes': settings.OTP_EXPIRY_MINUTES
                })
                plain_message = f"Your verification code is: {otp_code}. This code expires in {settings.OTP_EXPIRY_MINUTES} minutes."
                
                send_mail(
                    subject=subject,
                    message=plain_message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[user.email],
                    html_message=html_message,
                    fail_silently=False,
                )
                print(f"New verification OTP for {user.email}: {otp_code}")
            except Exception as e:
                print(f"Failed to send verification email: {e}")
                print(f"New verification OTP for {user.email}: {otp_code}")
            
            messages.success(request, 'New verification code sent to your email.')
            return redirect('accounts:verify_email')
            
        except User.DoesNotExist:
            messages.error(request, 'User not found.')
            return redirect('accounts:verify_email')


class PasswordResetRequestView(TemplateView):
    """
    Password reset request view.
    """
    template_name = 'accounts/password_reset.html'
    
    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        
        try:
            user = User.objects.get(email=email)
            
            # Generate password reset OTP
            otp_code = ''.join(random.choices(string.digits, k=6))
            expires_at = timezone.now() + timedelta(minutes=settings.OTP_EXPIRY_MINUTES)
            
            OTP.objects.create(
                user=user,
                otp_code=otp_code,
                purpose='password_reset',
                expires_at=expires_at
            )
            
            # Send email
            try:
                from django.core.mail import send_mail
                from django.template.loader import render_to_string
                
                subject = 'Password Reset - Course Registration System'
                html_message = render_to_string('accounts/emails/password_reset_email.html', {
                    'user': user,
                    'otp_code': otp_code,
                    'expiry_minutes': settings.OTP_EXPIRY_MINUTES
                })
                plain_message = f"Your password reset code is: {otp_code}. This code expires in {settings.OTP_EXPIRY_MINUTES} minutes."
                
                send_mail(
                    subject=subject,
                    message=plain_message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[user.email],
                    html_message=html_message,
                    fail_silently=False,
                )
                print(f"Password reset OTP for {user.email}: {otp_code}")
            except Exception as e:
                print(f"Failed to send password reset email: {e}")
                print(f"Password reset OTP for {user.email}: {otp_code}")
            
            messages.success(request, 'Password reset code sent to your email.')
            return redirect('accounts:password_reset_confirm')
            
        except User.DoesNotExist:
            messages.error(request, 'User with this email does not exist.')
            return render(request, self.template_name)


class PasswordResetConfirmView(TemplateView):
    """
    Password reset confirmation view.
    """
    template_name = 'accounts/password_reset_confirm.html'
    
    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        otp_code = request.POST.get('otp_code')
        new_password = request.POST.get('new_password')
        password_confirm = request.POST.get('password_confirm')
        
        if new_password != password_confirm:
            messages.error(request, 'Passwords do not match.')
            return render(request, self.template_name)
        
        try:
            user = User.objects.get(email=email)
            otp = OTP.objects.filter(
                user=user,
                otp_code=otp_code,
                purpose='password_reset',
                is_used=False
            ).first()
            
            if otp and otp.is_valid:
                # Reset password
                user.set_password(new_password)
                user.save()
                
                # Mark OTP as used
                otp.is_used = True
                otp.save()
                
                messages.success(request, 'Password reset successfully! You can now log in.')
                return redirect('accounts:login')
            else:
                messages.error(request, 'Invalid or expired OTP.')
                return render(request, self.template_name)
                
        except User.DoesNotExist:
            messages.error(request, 'User not found.')
            return render(request, self.template_name)
