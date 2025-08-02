from django.urls import path
from . import views

app_name = 'modules'

urlpatterns = [
    path('', views.module_list_view, name='module_list'),
    path('<int:module_id>/', views.module_detail_view, name='module_detail'),
    path('search/', views.module_search_view, name='module_search'),
]
