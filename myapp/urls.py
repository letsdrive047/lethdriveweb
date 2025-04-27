from django.contrib import admin
from django.urls import path,include
from myapp import views

from django.contrib.auth import views as auth_views
from django.contrib.auth import logout


urlpatterns = [
    path('', views.index, name='index'),
    path('register_employee/', views.register_employee, name='register_employee'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('driver_login/', views.driver_login, name='driver_login'),
    path('patner_login/', views.patner_login, name='patner_login'),
    path('admin_login/', views.admin_login, name='admin_login'),
    path('my_current_booking/', views.my_current_booking, name='my_current_booking'),
    path('logout/', views.employee_logout, name='employee_logout'),
    path('driver_dashboard/', views.driver_dashboard, name='driver_dashboard'),
    path('driver_profile/', views.driver_profile, name='driver_profile'),
    path('velet_bookings/', views.velet_bookings, name='velet_bookings'),
    path('bus_bookings/', views.bus_bookings, name='bus_bookings'),
    path('driving_class_bookings/', views.driving_class_bookings, name='driving_class_bookings'),
    path('monthly_bookings/', views.monthly_bookings, name='monthly_bookings'),
    path('weakly_bookings/', views.weakly_bookings, name='weakly_bookings'),
    path('my_weakly_bookings/', views.my_weakly_bookings, name='my_weakly_bookings'),
    path('hourly_bookings/', views.hourly_bookings, name='hourly_bookings'),
    path('my_hourly_bookings/', views.my_hourly_bookings, name='my_hourly_bookings'),
    path('my_bookings/', views.my_bookings, name='my_bookings'),
    path('update_booking_status_gen/<str:collection>/', views.update_booking_status_gen, name='update_booking_status_gen'),
   
    path('update_booking_amount/<str:collection>/', views.update_booking_amount, name='update_booking_amount'),
    
    
]
  
