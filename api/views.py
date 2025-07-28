from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend
from students.models import Student
from modules.models import Module, Registration
from rest_framework import serializers
import requests


# Pagination
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


# Serializers
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']


class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Student
        fields = ['id', 'user', 'date_of_birth', 'address', 'city', 'country', 'photo', 'is_email_verified']


class ModuleSerializer(serializers.ModelSerializer):
    registered_students_count = serializers.ReadOnlyField()
    available_spots = serializers.ReadOnlyField()
    is_full = serializers.ReadOnlyField()
    
    class Meta:
        model = Module
        fields = ['id', 'name', 'code', 'credit', 'category', 'description', 'availability', 
                 'max_students', 'registered_students_count', 'available_spots', 'is_full']


class RegistrationSerializer(serializers.ModelSerializer):
    student = StudentSerializer(read_only=True)
    module = ModuleSerializer(read_only=True)
    
    class Meta:
        model = Registration
        fields = ['id', 'student', 'module', 'date_registered']


# ViewSets
class ModuleViewSet(viewsets.ReadOnlyModelViewSet):
    """API viewset for modules with pagination and filtering"""
    queryset = Module.objects.filter(availability=True)
    serializer_class = ModuleSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'credit', 'availability']
    search_fields = ['name', 'code', 'description']
    ordering_fields = ['name', 'code', 'credit', 'created_at']
    ordering = ['name']
    
    @action(detail=True, methods=['get'])
    def registrations(self, request, pk=None):
        """Get registrations for a specific module"""
        module = self.get_object()
        registrations = module.registrations.all()
        serializer = RegistrationSerializer(registrations, many=True)
        return Response(serializer.data)


class StudentViewSet(viewsets.ReadOnlyModelViewSet):
    """API viewset for students with pagination and filtering"""
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_email_verified', 'city', 'country']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'user__email']
    ordering_fields = ['user__username', 'user__date_joined']
    ordering = ['user__username']
    
    @action(detail=True, methods=['get'])
    def modules(self, request, pk=None):
        """Get modules for a specific student"""
        student = self.get_object()
        registrations = student.registrations.all()
        serializer = RegistrationSerializer(registrations, many=True)
        return Response(serializer.data)


class RegistrationViewSet(viewsets.ReadOnlyModelViewSet):
    """API viewset for registrations with pagination and filtering"""
    queryset = Registration.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['module__category', 'module__credit']
    search_fields = ['student__user__username', 'module__name', 'module__code']
    ordering_fields = ['date_registered', 'module__name']
    ordering = ['-date_registered']

