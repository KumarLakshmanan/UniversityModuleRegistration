from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_http_methods
from django.db.models import Q
from rest_framework import viewsets, status, generics, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from students.models import Student, OTP
from modules.models import Module
from registrations.models import Registration
from sitecore.models import ContactMessage, SystemStats
from .serializers import (
    StudentSerializer, StudentCreateSerializer,
    ModuleSerializer, ModuleListSerializer,
    RegistrationSerializer, RegistrationListSerializer,
    ContactMessageSerializer, SystemStatsSerializer,
    UserSerializer
)


@api_view(['GET'])
@permission_classes([AllowAny])
def api_root(request):
    """
    API root endpoint providing information about available endpoints.
    """
    return Response({
        'message': 'Welcome to Course Registration System API',
        'endpoints': {
            'students': '/api/students/',
            'modules': '/api/modules/',
            'registrations': '/api/registrations/',
            'auth': {
                'register': '/api/auth/register/',
                'login': '/api/auth/login/',
                'logout': '/api/auth/logout/',
                'verify_email': '/api/auth/verify-email/',
                'password_reset': '/api/auth/password-reset/',
            },
            'stats': '/api/stats/',
            'contact': '/api/contact/',
        }
    })


class StudentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing student profiles.
    """
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Students can only view their own profile
        if self.request.user.is_staff:
            return Student.objects.all()
        return Student.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        if self.action == 'create':
            return StudentCreateSerializer
        return StudentSerializer


class ModuleViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing modules.
    """
    queryset = Module.objects.filter(status='active')
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'code', 'description', 'category']
    ordering_fields = ['name', 'code', 'credits']
    ordering = ['name']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ModuleListSerializer
        return ModuleSerializer


class RegistrationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing registrations.
    """
    queryset = Registration.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Students can only view their own registrations
        if self.request.user.is_staff:
            return Registration.objects.all()
        
        try:
            student = self.request.user.student_profile
            return Registration.objects.filter(student=student, is_active=True)
        except:
            return Registration.objects.none()
    
    def get_serializer_class(self):
        if self.action == 'list':
            return RegistrationListSerializer
        return RegistrationSerializer
    
    def perform_destroy(self, instance):
        # Instead of deleting, mark as withdrawn
        instance.status = 'withdrawn'
        instance.is_active = False
        instance.save()


class RegisterAPIView(APIView):
    """
    API endpoint for user registration.
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        # Implementation will be added later
        return Response({'message': 'Registration endpoint'})


class LoginAPIView(APIView):
    """
    API endpoint for user login.
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        # Implementation will be added later
        return Response({'message': 'Login endpoint'})


class LogoutAPIView(APIView):
    """
    API endpoint for user logout.
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        logout(request)
        return Response({'message': 'Logged out successfully'})


class VerifyEmailAPIView(APIView):
    """
    API endpoint for email verification.
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        # Implementation will be added later
        return Response({'message': 'Email verification endpoint'})


class PasswordResetAPIView(APIView):
    """
    API endpoint for password reset request.
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        # Implementation will be added later
        return Response({'message': 'Password reset endpoint'})


class PasswordResetConfirmAPIView(APIView):
    """
    API endpoint for password reset confirmation.
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        # Implementation will be added later
        return Response({'message': 'Password reset confirm endpoint'})


class ModuleRegisterAPIView(APIView):
    """
    API endpoint for module registration.
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request, code):
        try:
            module = Module.objects.get(code=code)
            student = request.user.student_profile
            
            # Check if already registered
            if Registration.objects.filter(student=student, module=module, is_active=True).exists():
                return Response({'success': False, 'message': 'Already registered for this module'})
            
            # Check if module allows registration
            if not module.can_register():
                return Response({'success': False, 'message': 'Module not available for registration'})
            
            # Create registration
            Registration.objects.create(student=student, module=module)
            
            return Response({'success': True, 'message': 'Successfully registered for module'})
            
        except Module.DoesNotExist:
            return Response({'success': False, 'message': 'Module not found'})
        except Exception as e:
            return Response({'success': False, 'message': 'Registration failed'})


class ModuleUnregisterAPIView(APIView):
    """
    API endpoint for module unregistration.
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request, code):
        try:
            module = Module.objects.get(code=code)
            student = request.user.student_profile
            
            registration = Registration.objects.filter(
                student=student, 
                module=module, 
                is_active=True
            ).first()
            
            if not registration:
                return Response({'success': False, 'message': 'Not registered for this module'})
            
            registration.withdraw()
            
            return Response({'success': True, 'message': 'Successfully unregistered from module'})
            
        except Module.DoesNotExist:
            return Response({'success': False, 'message': 'Module not found'})
        except Exception as e:
            return Response({'success': False, 'message': 'Unregistration failed'})


class APIDocsView(APIView):
    """
    API documentation view.
    """
    permission_classes = [AllowAny]
    
    def get(self, request):
        return render(request, 'api/docs.html')


class ContactAPIView(generics.CreateAPIView):
    """
    API endpoint for contact form submissions.
    """
    serializer_class = ContactMessageSerializer
    permission_classes = [AllowAny]
    
    def perform_create(self, serializer):
        serializer.save()


class SystemStatsAPIView(generics.ListAPIView):
    """
    API endpoint for system statistics.
    """
    serializer_class = SystemStatsSerializer
    permission_classes = [AllowAny]
    queryset = SystemStats.objects.all().order_by('-last_updated')
    
    def get_queryset(self):
        # Return only the latest stats
        return SystemStats.objects.all().order_by('-last_updated')[:1]


class UserProfileAPIView(generics.RetrieveUpdateAPIView):
    """
    API endpoint for current user profile.
    """
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return self.request.user


class ModuleRegistrationAPIView(APIView):
    """
    API endpoint for module registration/unregistration.
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request, module_id):
        """Register for a module."""
        try:
            module = get_object_or_404(Module, id=module_id, status='active')
            student = request.user.student_profile
            
            # Check if can register
            if not module.can_register():
                return Response(
                    {'error': 'Cannot register for this module'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Check for existing registration
            if Registration.objects.filter(
                student=student, module=module, is_active=True
            ).exists():
                return Response(
                    {'error': 'Already registered for this module'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Create registration
            registration = Registration.objects.create(
                student=student,
                module=module,
                status='enrolled'
            )
            
            serializer = RegistrationSerializer(registration)
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        except Student.DoesNotExist:
            return Response(
                {'error': 'Student profile not found'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def delete(self, request, module_id):
        """Unregister from a module."""
        try:
            module = get_object_or_404(Module, id=module_id)
            student = request.user.student_profile
            
            registration = get_object_or_404(
                Registration,
                student=student,
                module=module,
                is_active=True
            )
            
            # Mark as withdrawn instead of deleting
            registration.status = 'withdrawn'
            registration.is_active = False
            registration.save()
            
            return Response(
                {'message': 'Successfully unregistered from module'}, 
                status=status.HTTP_200_OK
            )
            
        except Student.DoesNotExist:
            return Response(
                {'error': 'Student profile not found'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        except Registration.DoesNotExist:
            return Response(
                {'error': 'Registration not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ModuleRegisterByCodeAPIView(APIView):
    """
    API endpoint for student registration by module code.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, code):
        try:
            module = get_object_or_404(Module, code=code, status='active')
            student = request.user.student_profile

            # Check if can register
            if hasattr(module, 'can_register') and callable(module.can_register):
                can_register = module.can_register()
            else:
                can_register = True
            if not can_register:
                return Response({'error': 'Cannot register for this module'}, status=status.HTTP_400_BAD_REQUEST)

            # Check for existing registration (active or inactive)
            reg = Registration.objects.filter(student=student, module=module).first()
            if reg:
                if reg.is_active:
                    return Response({'error': 'Already registered for this module'}, status=status.HTTP_400_BAD_REQUEST)
                # Reactivate withdrawn registration
                reg.is_active = True
                reg.status = 'enrolled'
                reg.withdrawal_date = None
                reg.withdrawal_reason = ''
                reg.completion_date = None
                reg.grade = ''
                reg.save()
                serializer = RegistrationSerializer(reg)
                return Response(serializer.data, status=status.HTTP_200_OK)

            # Create registration if none exists
            registration = Registration.objects.create(
                student=student,
                module=module,
                status='enrolled',
                is_active=True
            )
            serializer = RegistrationSerializer(registration)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Student.DoesNotExist:
            return Response({'error': 'Student profile not found'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ModuleUnregisterByCodeAPIView(APIView):
    """
    API endpoint for student unregistration by module code.
    """
    permission_classes = [IsAuthenticated]

    def delete(self, request, code):
        return self._unregister(request, code)

    def post(self, request, code):
        return self._unregister(request, code)

    def _unregister(self, request, code):
        try:
            module = get_object_or_404(Module, code=code)
            student = request.user.student_profile
            registration = get_object_or_404(
                Registration,
                student=student,
                module=module,
                is_active=True
            )
            # Mark as withdrawn instead of deleting
            registration.status = 'withdrawn'
            registration.is_active = False
            registration.save()
            return Response({
                'status': 'unregistered',
                'message': 'Successfully unregistered from module'}, status=status.HTTP_200_OK)
        except Student.DoesNotExist:
            return Response({'error': 'Student profile not found'}, status=status.HTTP_400_BAD_REQUEST)
        except Registration.DoesNotExist:
            return Response({'error': 'Registration not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
