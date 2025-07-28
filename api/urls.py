from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from . import views

app_name = 'api'

router = DefaultRouter()
router.register(r'modules', views.ModuleViewSet)
router.register(r'students', views.StudentViewSet)
router.register(r'registrations', views.RegistrationViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/token/', obtain_auth_token, name='token'),
]
