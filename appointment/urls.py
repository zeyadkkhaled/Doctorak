from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
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
    path('change_profile_picture/', views.change_profile_picture, name='change_profile_picture'),
    path('profile/', views.profile_view, name='profile'),
    path('patient/<str:patient_id>/edit', views.edit_patient_profile, name='edit_patient_profile'),
    path('patient/<str:patient_id>/edit_medical_history', views.edit_medical_history, name='edit_medical_history'),
    path('doctors/', views.doctor_list, name='doctor_list'),
    path('doctor_info/<str:doctor_id>/', views.doctor_info, name='doctor_info'),
    path('doctor/<str:appointment_id>/appointments/', views.appointment_status, name='appointment_status'),
    path('doctor-patient-view/<str:patient_id>/', views.doctor_patient_view, name='doctor_patient_view'),
    path('save-prescription/', views.save_prescription, name='save_prescription'),
    path('save_review/', views.save_review, name='save_review'),
    path('adminregister/',views.adminregister,name='adminregister'),
    path('adminlogin/<str:admin_id>',views.admin_profile,name='admin_profile'),
    path('admin/edit-admin/<int:admin_id>/', views.edit_admin, name='edit_admin'),
    path('admin/edit-doctor/<int:doctor_id>/', views.edit_doctor_admin, name='edit_doctor_admin'),
    path('admin/edit-patient/<int:patient_id>/', views.edit_patient_admin, name='edit_patient_admin'),
    path('admin/edit-appointment/<int:appointment_id>/', views.edit_appointment_admin, name='edit_appointment_admin'),
]
