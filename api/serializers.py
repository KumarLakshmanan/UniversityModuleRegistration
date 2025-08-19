from rest_framework import serializers
from django.contrib.auth.models import User
from students.models import Student, OTP
from modules.models import Course, Module
from registrations.models import Registration
from sitecore.models import ContactMessage, SystemStats


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model."""
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'date_joined']
        read_only_fields = ['id', 'date_joined']


class StudentSerializer(serializers.ModelSerializer):
    """Serializer for Student model."""
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Student
        fields = [
            'id', 'user', 'date_of_birth', 'phone', 
            'address', 'city', 'country', 'photo', 'is_verified', 'created_at'
        ]
        read_only_fields = ['id', 'is_verified', 'created_at']


class StudentCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating a new student with user."""
    user = UserSerializer()
    
    class Meta:
        model = Student
        fields = [
            'user', 'date_of_birth', 'phone', 'address', 'city', 'country', 'photo'
        ]
    
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data)
        student = Student.objects.create(user=user, **validated_data)
        return student


class ModuleSerializer(serializers.ModelSerializer):
    """Serializer for Module model."""
    full_code = serializers.SerializerMethodField()
    course_title = serializers.SerializerMethodField()
    enrolled_count = serializers.SerializerMethodField()
    can_register = serializers.SerializerMethodField()
    
    class Meta:
        model = Module
        fields = [
            'id', 'code', 'name', 'description', 'credits', 'category',
            'prerequisites', 'status', 'is_available_for_registration', 'max_students',
            'created_at', 'updated_at', 'full_code', 'course_title', 'enrolled_count',
            'can_register'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_full_code(self, obj):
        """Get the full module code including course code."""
        return obj.full_code
    
    def get_course_title(self, obj):
        """Get the course title."""
        return obj.course.title
    
    def get_enrolled_count(self, obj):
        """Get the number of students enrolled in this specific module."""
        from registrations.models import Registration
        return Registration.objects.filter(module=obj, is_active=True).count()
    
    def get_can_register(self, obj):
        """Check if current user can register for this module."""
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return obj.can_register()
        
        try:
            student = request.user.student_profile
            from registrations.models import Registration
            already_registered = Registration.objects.filter(
                student=student, module=obj, is_active=True
            ).exists()
            return obj.can_register() and not already_registered
        except:
            return obj.can_register()


class CourseSerializer(serializers.ModelSerializer):
    """Serializer for Course model."""
    enrolled_count = serializers.SerializerMethodField()
    total_credits = serializers.SerializerMethodField()
    module_count = serializers.SerializerMethodField()
    is_registration_open = serializers.SerializerMethodField()
    can_register = serializers.SerializerMethodField()
    modules = ModuleSerializer(many=True, read_only=True)
    
    class Meta:
        model = Course
        fields = [
            'id', 'course_code', 'title', 'description', 'status', 
            'is_available_for_registration', 'created_at', 'updated_at',
            'enrolled_count', 'total_credits', 'module_count', 'is_registration_open', 
            'can_register', 'modules'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_enrolled_count(self, obj):
        """Get the number of enrolled students."""
        return obj.enrolled_students_count
    
    def get_total_credits(self, obj):
        """Get total credits for this course."""
        return obj.total_credits
    
    def get_module_count(self, obj):
        """Get number of modules in this course."""
        return obj.module_count
    
    def get_is_registration_open(self, obj):
        """Check if registration is currently open."""
        return obj.is_available_for_registration
    
    def get_can_register(self, obj):
        """Check if current user can register for this course."""
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return False
        
        try:
            student = request.user.student_profile
            return obj.can_register() and not obj.registrations.filter(
                student=student, is_active=True
            ).exists()
        except:
            return False


class CourseListSerializer(serializers.ModelSerializer):
    """Simplified serializer for course list views."""
    enrolled_count = serializers.SerializerMethodField()
    total_credits = serializers.SerializerMethodField()
    module_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Course
        fields = [
            'id', 'course_code', 'title', 'description', 'status', 
            'enrolled_count', 'total_credits', 'module_count'
        ]
    
    def get_enrolled_count(self, obj):
        return obj.enrolled_students_count
    
    def get_total_credits(self, obj):
        return obj.total_credits
    
    def get_module_count(self, obj):
        return obj.module_count


class ModuleListSerializer(serializers.ModelSerializer):
    """Simplified serializer for module list views."""
    full_code = serializers.SerializerMethodField()
    course_title = serializers.SerializerMethodField()
    
    class Meta:
        model = Module
        fields = [
            'id', 'code', 'name', 'credits', 'category', 
            'max_students', 'status', 'full_code', 'course_title'
        ]
    
    def get_full_code(self, obj):
        return obj.full_code
    
    def get_course_title(self, obj):
        return obj.course.title


class RegistrationSerializer(serializers.ModelSerializer):
    """Serializer for Registration model."""
    student = StudentSerializer(read_only=True)
    module = ModuleSerializer(read_only=True)
    module_id = serializers.IntegerField(write_only=True)
    module_credits = serializers.SerializerMethodField()
    
    class Meta:
        model = Registration
        fields = [
            'id', 'student', 'module', 'module_id', 'status', 
            'date_registered', 'completion_date', 'grade', 'is_active', 'module_credits'
        ]
        read_only_fields = ['id', 'student', 'date_registered', 'completion_date']
    
    def get_module_credits(self, obj):
        """Get credits for this module registration."""
        return obj.module.credits
    
    def create(self, validated_data):
        """Create a new registration."""
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            raise serializers.ValidationError("Authentication required.")
        
        try:
            student = request.user.student_profile
        except Student.DoesNotExist:
            raise serializers.ValidationError("Student profile not found.")
        
        module_id = validated_data.pop('module_id')
        try:
            module = Module.objects.get(id=module_id, status='active')
        except Module.DoesNotExist:
            raise serializers.ValidationError("Module not found or inactive.")
        
        # Check if student can register
        if not module.can_register():
            raise serializers.ValidationError("Cannot register for this module.")
        
        # Check for existing registration
        if Registration.objects.filter(
            student=student, module=module, is_active=True
        ).exists():
            raise serializers.ValidationError("Already registered for this module.")
        
        validated_data['student'] = student
        validated_data['module'] = module
        return super().create(validated_data)


class RegistrationListSerializer(serializers.ModelSerializer):
    """Simplified serializer for registration list views."""
    module = ModuleListSerializer(read_only=True)
    student_name = serializers.SerializerMethodField()
    module_credits = serializers.SerializerMethodField()
    
    class Meta:
        model = Registration
        fields = [
            'id', 'module', 'student_name', 'status', 
            'date_registered', 'grade', 'is_active', 'module_credits'
        ]
    
    def get_student_name(self, obj):
        return f"{obj.student.user.first_name} {obj.student.user.last_name}".strip()
    
    def get_module_credits(self, obj):
        return obj.module.credits


class ContactMessageSerializer(serializers.ModelSerializer):
    """Serializer for ContactMessage model."""
    
    class Meta:
        model = ContactMessage
        fields = [
            'id', 'name', 'email', 'phone', 'subject', 'message', 
            'is_read', 'is_replied', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class SystemStatsSerializer(serializers.ModelSerializer):
    """Serializer for SystemStats model."""
    
    class Meta:
        model = SystemStats
        fields = [
            'id', 'total_students', 'total_modules', 'total_registrations',
            'active_modules', 'last_updated'
        ]
        read_only_fields = ['id', 'last_updated']


class OTPSerializer(serializers.ModelSerializer):
    """Serializer for OTP model (admin use only)."""
    user = UserSerializer(read_only=True)
    is_valid = serializers.SerializerMethodField()
    
    class Meta:
        model = OTP
        fields = [
            'id', 'user', 'purpose', 'is_used', 'expires_at', 
            'created_at', 'is_valid'
        ]
        read_only_fields = ['id', 'created_at']
    
    def get_is_valid(self, obj):
        return obj.is_valid


# API Response Serializers
class SuccessResponseSerializer(serializers.Serializer):
    """Standard success response."""
    message = serializers.CharField()
    data = serializers.JSONField(required=False)


class ErrorResponseSerializer(serializers.Serializer):
    """Standard error response."""
    error = serializers.CharField()
    details = serializers.CharField(required=False)
    code = serializers.CharField(required=False)


class PaginatedResponseSerializer(serializers.Serializer):
    """Paginated response wrapper."""
    count = serializers.IntegerField()
    next = serializers.URLField(allow_null=True)
    previous = serializers.URLField(allow_null=True)
    results = serializers.ListField()
