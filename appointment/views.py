from django.shortcuts import redirect
from .forms import DoctorRegisterForm
from .models import User, Doctor, Clinic
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import authenticate, login,get_user_model


def home(request):
    return render(request, 'home.html')


def doctor_register(request):
        if request.method == 'POST':
            form = DoctorRegisterForm(request.POST)
            if form.is_valid():
                # Create user first
                user = User.objects.create_user(
                    email=form.cleaned_data['email'],
                    password=form.cleaned_data['password'],
                    role='doctor'
                )

                # Create doctor profile
                Doctor.objects.create(
                    user=user,
                    f_name=form.cleaned_data['f_name'],
                    l_name=form.cleaned_data['l_name'],
                    gender=form.cleaned_data['gender'],
                    dob=form.cleaned_data['dob'],
                    phone=form.cleaned_data['phone'],
                    address=form.cleaned_data['address'],
                    speciality=form.cleaned_data['speciality'],
                    experience=form.cleaned_data['experience'],
                )
                return redirect('doctor_register_success')
        else:
            form = DoctorRegisterForm()
        return render(request, 'doctor_register.html', {'form': form})

def doctor_register_success(request):
    return render(request, 'success.html')


def register(request):
    return render(request, 'signup.html')


def loginPage(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)  # Authenticate the user
        if user:
            login(request, user) # Log the user in and create a session
            if user.role == 'doctor':
                return render(request, 'success.html')
            elif user.role == 'patient':
                return redirect('patient_dashboard')
            elif user.role == 'admin':
                return redirect('admin_dashboard')
        else:
            messages.error(request, "Invalid credentials.")

    return render(request, 'signin.html')