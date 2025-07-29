from django.urls import path
from . import views

app_name = 'registrations'

urlpatterns = [
    # Student registrations
    path('my-modules/', views.MyModulesView.as_view(), name='my_modules'),
]
