"""project_3 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from my_work import views
from my_work.views import OTPVerifyView  # Ensure to import your views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.HomeView.as_view(), name='home'),
    path('admin/home/', views.AdminHomeView.as_view(), name='home_3'),
    path('student/home/', views.StudentHomeView.as_view(), name='home_1'),
    path('teacher/home', views.TeachersHomeView.as_view(), name='home_2'),
    path('phone_number/', views.PhoneNumberView.as_view(), name='phone_number'),
    path('verify_otp/', views.OTPVerifyView.as_view(), name='verify_otp'),
    path('register/', views.UserRegisterView.as_view(), name='register'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path("logout/",views.Signout.as_view(),name="lgout"),
    path("login/",views.CustomLoginView.as_view(),name="lgn"),
    path("add/class/",views.AddClassView.as_view(),name="class"),
    path('classmodel/update/<int:pk>', views.ClassModelUpdateView.as_view(), name='classmodel-update'),
    path('verify_otp/', OTPVerifyView.as_view(), name='verify_otp'),
    # path('success/', SuccessView.as_view(), name='success_url'),  # Success redirect


]