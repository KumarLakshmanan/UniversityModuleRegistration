from django.urls import path
from . import views

app_name = 'sitecore'

urlpatterns = [
    # Static pages
    path('', views.HomeView.as_view(), name='home'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('unauthorized/', views.UnauthorizedView.as_view(), name='unauthorized'),
]
