from django.urls import path
from . import views

app_name = 'modules'

urlpatterns = [
    # Module browsing
    path('', views.ModuleListView.as_view(), name='list'),
    path('<slug:code>/', views.ModuleDetailView.as_view(), name='detail'),
    
    # Registration actions (AJAX)
    path('<int:pk>/register/', views.module_register, name='register'),
    path('<int:pk>/unregister/', views.module_unregister, name='unregister'),
]
