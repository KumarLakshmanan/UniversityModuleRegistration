from django.urls import path
from . import views

app_name = 'modules'

urlpatterns = [
    path('', views.ModuleListView.as_view(), name='list'),
    path('<slug:code>/', views.ModuleDetailView.as_view(), name='detail'),
    path('<slug:code>/register/', views.ModuleRegistrationView.as_view(), name='register'),
    path('<slug:code>/unregister/', views.ModuleUnregistrationView.as_view(), name='unregister'),
]
