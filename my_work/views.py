
from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView, CreateView,View,UpdateView
from django.contrib.auth.views import LoginView

from django.shortcuts import render
from my_work.models import *
from django.shortcuts import render, redirect
from my_work.forms import *
from .models import User
from django_otp.oath import totp
from twilio.rest import Client
from django.contrib.auth import authenticate, login, logout
from phonenumbers import parse, is_valid_number, format_number, PhoneNumberFormat
from .forms import PhoneNumberForm
import pyotp
from .forms import OTPForm



# Create your views here.
account_sid = 'AC6efab8ae589fb0ae07c5f09dff180213'
auth_token = 'c239ab8824e0c8639361f38d30941ee0'
client = Client(account_sid, auth_token)



class HomeView(TemplateView):
    template_name = 'home.html'


class AdminHomeView(TemplateView):
    template_name = 'AdminHomeView.html'

class TeachersHomeView(TemplateView):
    template_name = 'TeachersHomeView.html'

class StudentHomeView(TemplateView):
    template_name = 'StudentHomeView.html'




class PhoneNumberView(FormView):
    template_name = 'phone_number.html'
    form_class = PhoneNumberForm
    success_url = reverse_lazy('verify_otp')

    def form_valid(self, form):
        mobile = form.cleaned_data['mobile']
        
        # Generate a new OTP
        secret = pyotp.random_base32()  # You should store this in your user model or session
        totp = pyotp.TOTP(secret)
        otp = totp.now()

        try:
            # Send the OTP via SMS (using your Twilio logic)
            verification = client.verify \
                .v2 \
                .services('VAf62bb1bf39423431c4b865dcffd4efcc') \
                .verifications \
                .create(to=mobile, channel='sms')

            # Store mobile number and OTP in session for verification
            self.request.session['mobile'] = mobile
            self.request.session['otp'] = otp  # Store the generated OTP
            self.request.session['secret'] = secret  # Store the secret for later verification
        except Exception as e:
            form.add_error(None, f"Error sending OTP: {str(e)}")
            return self.form_invalid(form)

        return super().form_valid(form)


class OTPVerifyView(View):
    def get(self, request):
        form = OTPForm()
        return render(request, 'verify_otp.html', {'form': form})

    def post(self, request):
        form = OTPForm(request.POST)
        if form.is_valid():
            # Your verification logic here
            return redirect('register')  # Change this to your success redirect
        return render(request, 'verify_otp.html', {'form': form})


class UserRegisterView(View):
    def get(self, request, *args, **kwargs):
        form = UserForm()
        return render(request, "register.html", {"form": form})

    def post(self, request, *args, **kwargs):
        form = UserForm(request.POST)
        if form.is_valid():
            user = CustomUser.objects.create_user(**form.cleaned_data)
            user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect("profile")
        return render(request, "register.html", {"form": form})

    

class ProfileView(View):
    def get(self, request, *args, **kwargs):
        user_type = request.user.user_type

        if user_type == 'teacher':
            form = TeacherForm()
        else:
            form = StudentForm()

        return render(request, 'profile_form.html', {'form': form})

    def post(self, request, *args, **kwargs):
        user_type = request.user.user_type
        print(f"User type: {user_type}")

        # Bind the correct form based on the user type
        if user_type == 'teacher':
            form = TeacherForm(request.POST, request.FILES)
            if form.is_valid():
                profile, created = Profile.objects.get_or_create(user=request.user)
                for field, value in form.cleaned_data.items():
                    setattr(profile, field, value)
                profile.save()
                return redirect('home_2')
        else:
            form = StudentForm(request.POST)

            if form.is_valid():
                profile, created = Profile.objects.get_or_create(user=request.user)
                for field, value in form.cleaned_data.items():
                    setattr(profile, field, value)
                profile.save()
                return redirect('home')  
        # If form is not valid, re-render the form with errors
        return render(request, 'profile_form.html', {'form': form})  

        




class Signout(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        return redirect('lgn')
    


class CustomLoginView(LoginView):
    template_name = 'login.html'
    authentication_form = CustomAuthenticationForm
    redirect_authenticated_user = True

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        if self.request.user.is_staff :
            return redirect('home_1')  
        elif user.user_type == 'student':
            return redirect('home_2')  
        elif user.user_type == 'teacher':
            return redirect('home_3')     
        else:
            return redirect(self.success_url)
        



class AddClassView(View):
    template_name = 'AddClassView.html'
    success_url = reverse_lazy('home_2')

    def get(self, request, *args, **kwargs):
        class_form = ClassForm1()
        discount_form = ClassForm2()
        return render(request, self.template_name, {
            'class_form': class_form,
            'discount_form': discount_form
        })

    def post(self, request, *args, **kwargs):
        class_form = ClassForm1(request.POST)
        discount_form = ClassForm2(request.POST)

        if class_form.is_valid() and discount_form.is_valid():
            # Save both forms
            class_instance = class_form.save(commit=False)
            class_instance.user = request.user
            class_instance.save()

            discount_instance = discount_form.save(commit=False)
            discount_instance.user = request.user
            discount_instance.save()

            return redirect(self.success_url)
        else:
            # If forms are not valid, re-render the page with forms and errors
            return render(request, self.template_name, {
                'class_form': class_form,
                'discount_form': discount_form
            })
        



class ClassModelUpdateView(UpdateView):
    model = ClassModel
    form_class = ClassForm2  
    template_name = 'ClassModelUpdateView.html'
    success_url = reverse_lazy('home_2')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user,  pk=self.kwargs['pk']) 



# class SuccessView(View):
#     def get(self, request):
#         return render(request, 'success.html')  # Make sure you have this template


