from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, FormView, CreateView, UpdateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse_lazy
from django.utils import timezone
from .models import Student, EmailVerification, PasswordResetOTP
from modules.models import Module, Registration
import json
import random
import string


class StudentRegistrationView(TemplateView):
    """Student registration view"""
    template_name = 'students/register.html'

    def post(self, request, *args, **kwargs):

        # Get form data
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')
        date_of_birth = request.POST.get('date_of_birth', '').strip()
        address = request.POST.get('address', '').strip()
        city = request.POST.get('city', '').strip()
        country = request.POST.get('country', '').strip()

        # Basic validation
        required_fields = {
            'username': username,
            'email': email,
            'password1': password1,
            'password2': password2,
            'date_of_birth': date_of_birth,
            'address': address,
            'city': city,
            'country': country
        }

        # Check for missing required fields
        missing_fields = [field for field,
                          value in required_fields.items() if not value]
        if missing_fields:
            messages.error(
                request, f'Please fill in all required fields: {", ".join(missing_fields)}')
            return render(request, self.template_name)

        if password1 != password2:
            messages.error(request, 'Passwords do not match.')
            return render(request, self.template_name)

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return render(request, self.template_name)

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
            return render(request, self.template_name)

        try:

            # Create user
            user = User.objects.create_user(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name,
                password=password1,
                is_active=False
                # User inactive until email verification
            )

            # Create student profile
            student_data = {
                'user': user,
                'date_of_birth': date_of_birth,
                'address': address,
                'city': city,
                'country': country
            }

            # Handle photo upload if provided
            if 'photo' in request.FILES:
                student_data['photo'] = request.FILES['photo']

            Student.objects.create(**student_data)

            # Send email verification OTP
            self.send_verification_email(user)

            messages.success(
                request, 'Registration successful! Please check your email for verification code.')
            return redirect('students:verify_email')

        except Exception as e:
            messages.error(request, f'Registration failed: {str(e)}')
            return render(request, self.template_name)

    def send_verification_email(self, user):
        """Send email verification OTP"""

        # Generate and save OTP
        verification = EmailVerification.objects.create(user=user)

        # Send email
        subject = 'Email Verification - University Module Registration'
        message = f'''
        Hello {user.first_name or user.username},
        
        Welcome to the University Module Registration System!
        
        Your email verification code is: {verification.otp}
        
        This code will expire in 10 minutes.
        
        Please enter this code on the verification page to activate your account.
        
        If you didn't create this account, please ignore this email.
        
        Best regards,
        University Registration Team
        '''

        try:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
        except Exception as e:
            print(f"Failed to send email: {e}")
            raise Exception("Failed to send verification email")


class StudentLoginView(LoginView):
    """Student login view"""
    template_name = 'students/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('students:dashboard')

    def form_valid(self, form):
        user = form.get_user()

        # Prevent admin/staff login on student portal
        if user.is_staff or user.is_superuser:
            messages.error(
                self.request, 'Admin users cannot login through the student portal. Please use the admin panel.')
            return self.form_invalid(form)

        # Check if user's email is verified
        if hasattr(user, 'student') and not user.student.is_email_verified:
            messages.warning(
                self.request, 'Please verify your email address before logging in.')
            return redirect('students:verify_email')

        return super().form_valid(form)


class StudentLogoutView(LogoutView):
    """Student logout view"""
    next_page = reverse_lazy('core:home')


class EmailVerificationView(TemplateView):
    """Email verification view"""
    template_name = 'students/verify_email.html'

    def post(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.POST.get('action') == 'resend':
            email = request.POST.get('email', '').strip()
            if not email:
                return JsonResponse({'success': False, 'message': 'Email is required.'})
            try:
                user = User.objects.get(email=email)

                # Invalidate previous OTPs
                EmailVerification.objects.filter(
                    user=user, is_used=False).update(is_used=True)
                verification = EmailVerification.objects.create(user=user)
                subject = 'Email Verification - University Module Registration'
                message = f"""
                Hello {user.first_name or user.username},

                Your new email verification code is: {verification.otp}

                This code will expire in 10 minutes.

                Best regards,
                University Registration Team
                """
                send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [
                          user.email], fail_silently=False)
                return JsonResponse({'success': True, 'message': 'A new verification code has been sent to your email.'})
            except Exception as e:
                return JsonResponse({'success': False, 'message': f'Failed to resend code: {str(e)}'})

        otp = request.POST.get('otp', '').strip()
        email = request.POST.get('email', '').strip()

        if not otp or not email:
            messages.error(
                request, 'Please provide both email and verification code.')
            return render(request, self.template_name)

        try:
            user = User.objects.get(email=email)
            verification = EmailVerification.objects.filter(
                user=user,
                otp=otp,
                is_used=False
            ).first()

            if not verification:
                messages.error(request, 'Invalid verification code.')
                return render(request, self.template_name)

            if verification.is_expired():
                messages.error(
                    request, 'Verification code has expired. Please request a new one.')
                return render(request, self.template_name)

            # Activate user account
            user.is_active = True
            user.save()

            # Mark verification as used
            verification.is_used = True
            verification.save()

            # Mark student email as verified
            user.student.is_email_verified = True
            user.student.save()

            messages.success(
                request, 'Email verified successfully! You can now log in.')
            return redirect('students:login')

        except User.DoesNotExist:
            messages.error(request, 'User with this email does not exist.')
            return render(request, self.template_name)
        except Exception as e:
            messages.error(request, f'Verification failed: {str(e)}')
            return render(request, self.template_name)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get email from query parameter if available
        context['email'] = self.request.GET.get('email', '')
        return context


class DashboardView(LoginRequiredMixin, TemplateView):
    """Student dashboard view"""
    template_name = 'students/dashboard.html'
    login_url = '/auth/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            student = self.request.user.student
            context['student'] = student
            context['registered_modules'] = student.registrations.all()[:5]
            context['total_modules'] = student.registrations.count()
            context['total_credits'] = sum(
                reg.module.credit for reg in student.registrations.all())
        except:
            context['student'] = None
        return context


class ProfileView(LoginRequiredMixin, TemplateView):
    """Student profile view"""
    template_name = 'students/profile.html'
    login_url = '/auth/login/'


class ProfileUpdateView(LoginRequiredMixin, TemplateView):
    """Student profile update view"""
    template_name = 'students/profile_edit.html'
    login_url = '/auth/login/'

    def post(self, request, *args, **kwargs):
        user = request.user

        # Update user fields
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.email = request.POST.get('email', '')
        user.save()

        # Update student profile if exists
        if hasattr(user, 'student'):
            student = user.student
            date_of_birth = request.POST.get('date_of_birth')
            if date_of_birth:
                student.date_of_birth = date_of_birth
            student.address = request.POST.get('address', '')
            student.city = request.POST.get('city', '')
            student.country = request.POST.get('country', '')

            if 'photo' in request.FILES:
                student.photo = request.FILES['photo']

            student.save()
        else:

            # Create student profile if it doesn't exist
            date_of_birth = request.POST.get('date_of_birth')
            if date_of_birth:
                Student.objects.create(
                    user=user,
                    date_of_birth=date_of_birth,
                    address=request.POST.get('address', ''),
                    city=request.POST.get('city', ''),
                    country=request.POST.get('country', '')
                )

            student.save()

        messages.success(request, 'Profile updated successfully!')
        return redirect('students:profile')


class MyModulesView(LoginRequiredMixin, TemplateView):
    """My modules view"""
    template_name = 'students/my_modules.html'
    login_url = '/auth/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            student = self.request.user.student
            registrations = student.registrations.all().order_by('-date_registered')

            # Add pagination
            from django.core.paginator import Paginator
            paginator = Paginator(registrations, 9)
            # 9 modules per page
            page_number = self.request.GET.get('page')
            page_obj = paginator.get_page(page_number)

            context['student'] = student
            context['registrations'] = page_obj
            context['is_paginated'] = page_obj.has_other_pages()
            context['page_obj'] = page_obj
        except:
            context['student'] = None
            context['registrations'] = []
        return context


class PasswordResetRequestView(TemplateView):
    """Password reset request view"""
    template_name = 'students/password_reset.html'

    def post(self, request, *args, **kwargs):
        email = request.POST.get('email', '').strip()

        if not email:
            messages.error(request, 'Please provide your email address.')
            return render(request, self.template_name)

        try:
            user = User.objects.get(email=email)

            # Generate and send OTP
            reset_otp = PasswordResetOTP.objects.create(user=user)

            # Send email
            subject = 'Password Reset - University Module Registration'
            message = f'''
            Hello {user.first_name or user.username},
            
            You have requested to reset your password for the University Module Registration System.
            
            Your password reset code is: {reset_otp.otp}
            
            This code will expire in 10 minutes.
            
            If you didn't request this password reset, please ignore this email.
            
            Best regards,
            University Registration Team
            '''

            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )

            messages.success(
                request, 'Password reset code sent to your email.')
            return redirect('students:password_reset_verify')

        except User.DoesNotExist:
            messages.error(request, 'No user found with this email address.')
            return render(request, self.template_name)
        except Exception as e:
            messages.error(request, f'Failed to send reset code: {str(e)}')
            return render(request, self.template_name)


class PasswordResetVerifyView(TemplateView):
    """Password reset verify view"""
    template_name = 'students/password_reset_verify.html'

    def post(self, request, *args, **kwargs):
        email = request.POST.get('email', '').strip()
        otp = request.POST.get('otp', '').strip()

        if not email or not otp:
            messages.error(
                request, 'Please provide both email and verification code.')
            return render(request, self.template_name)

        try:
            user = User.objects.get(email=email)
            reset_otp = PasswordResetOTP.objects.filter(
                user=user,
                otp=otp,
                is_used=False
            ).first()

            if not reset_otp:
                messages.error(request, 'Invalid reset code.')
                return render(request, self.template_name)

            if reset_otp.is_expired():
                messages.error(
                    request, 'Reset code has expired. Please request a new one.')
                return render(request, self.template_name)

            # Store verification in session for next step
            request.session['reset_user_id'] = user.id
            request.session['reset_otp_id'] = reset_otp.id

            return redirect('students:password_reset_confirm')

        except User.DoesNotExist:
            messages.error(request, 'User with this email does not exist.')
            return render(request, self.template_name)
        except Exception as e:
            messages.error(request, f'Verification failed: {str(e)}')
            return render(request, self.template_name)


class PasswordResetConfirmView(TemplateView):
    """Password reset confirm view"""
    template_name = 'students/password_reset_confirm.html'

    def get(self, request, *args, **kwargs):

        # Check if user has valid session from previous step
        if 'reset_user_id' not in request.session or 'reset_otp_id' not in request.session:
            messages.error(
                request, 'Invalid reset session. Please start the process again.')
            return redirect('students:password_reset')
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')

        if not password1 or not password2:
            messages.error(request, 'Please provide both password fields.')
            return render(request, self.template_name)

        if password1 != password2:
            messages.error(request, 'Passwords do not match.')
            return render(request, self.template_name)

        if len(password1) < 8:
            messages.error(
                request, 'Password must be at least 8 characters long.')
            return render(request, self.template_name)

        try:
            user_id = request.session.get('reset_user_id')
            otp_id = request.session.get('reset_otp_id')

            user = User.objects.get(id=user_id)
            reset_otp = PasswordResetOTP.objects.get(id=otp_id)

            # Mark OTP as used
            reset_otp.is_used = True
            reset_otp.save()

            # Update password
            user.set_password(password1)
            user.save()

            # Clear session
            del request.session['reset_user_id']
            del request.session['reset_otp_id']

            messages.success(
                request, 'Password reset successfully! You can now log in with your new password.')
            return redirect('students:login')

        except Exception as e:
            messages.error(request, f'Password reset failed: {str(e)}')
            return render(request, self.template_name)
