from django.urls import path
from . import views
from django.shortcuts import render

urlpatterns = [
    path('',views.home,name='home'),
    path('register/doctor/', views.doctor_register, name='doctor_register'),
    path('register/success/', lambda request: render(request, 'success.html'), name='doctor_register_success'),
    path('register/',views.register,name='register'),
    path('login/',views.loginPage,name='login'),
    path('articles.html',views.articles,name='articles'),
]
