from django.urls import path
from . import views

app_name = 'modules'

urlpatterns = [
    path('', views.module_list_view, name='module_list'),
    path('<int:module_id>/', views.module_detail_view, name='module_detail'),
    path('search/', views.module_search_view, name='module_search'),
    path('semester/<str:semester>/', views.modules_by_semester_view, name='modules_by_semester'),
]
