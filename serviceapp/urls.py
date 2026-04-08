import os
from django.urls import path # type: ignore
from . import views

urlpatterns = [
    path('', views.login_choice, name='login_choice'),
    path('admin-login/', views.admin_login, name='admin_login'),
    path('associate-login/', views.associate_login, name='associate_login'),
    path('login/service-incharge/', views.service_incharge_login, name='service_incharge_login'),  # ✅ Added line
    path('dashboard/', views.dashboard, name='dashboard'),
    path('service-incharge-dashboard/', views.service_incharge_dashboard, name='service_incharge_dashboard'),  # ✅ Added line for dashboard
    path('logout/', views.logout_view, name='logout'),
    path('add/', views.add_record, name='add_record'),
    path('edit/<int:pk>/', views.edit_record, name='edit_record'),
    path('delete/<int:pk>/', views.delete_record, name='delete_record'),
    path('service-records/', views.service_records, name='service_records'),
    path('under-service/', views.under_service, name='under_service'),
    path('under-service/add/', views.add_under_service, name='add_under_service'),
    path('under-service/edit/<int:pk>/', views.edit_under_service, name='edit_under_service'),
    path('service-due/', views.service_due, name='service_due'),
    # Add other URL patterns here...
]
