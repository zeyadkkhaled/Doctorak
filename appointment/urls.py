from django.urls import path
from . import views
from django.shortcuts import render

urlpatterns = [
    path('',views.home,name='home'),
    path('register/',views.register,name='register'),
    path('login/',views.loginPage,name='login'),
    path('articles.html',views.articles,name='articles'),
    path('logout/',views.logoutUser,name='logout'),
    path('doctor/<str:doctor_id>/', views.doctor_profile, name='doctor_profile'),
    path('patient/<str:patient_id>/', views.patient_profile, name='patient_profile'),
    path('doctor/<str:doctor_id>/edit/', views.edit_doctor_profile, name='edit_doctor_profile'),
    path('clinic/<str:clinic_id>/edit/', views.edit_clinic_profile, name='edit_clinic_profile'),
    path('exception/<str:exception_id>',views.edit_exception_hours, name='edit_exception_hours'),
    path('change-profile-picture/', views.change_profile_picture, name='change_profile_picture'),
]
