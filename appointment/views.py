#from email.utils import specialsre

from django.shortcuts import redirect
from .forms import DoctorRegisterForm
from .models import User, Doctor, Clinic, Patient
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import authenticate, login,get_user_model,logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required

def home(request):
    login_url= reverse('login')
    return render(request, 'home.html', {'login_url': login_url})


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
    message = request.GET.get('message')
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':

        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        gender = request.POST['gender']
        role = request.POST['role']
        dob = request.POST['dob']
        phone_number = request.POST['phone']
        address = request.POST['address']
        speciality = request.POST['speciality']
        experience = request.POST['experience']

        # Check if the email already exists
        if User.objects.filter(email=email).exists():
            return render(request, 'signup.html', {'message': "Email already exists."})
        else :
            if role == 'doctor':
                user = User.objects.create_user(
                    email=email,
                    password=password,
                    role='doctor',

                )

                # Create Doctor profile
                Doctor.objects.create(
                    user=user,
                    f_name=first_name,
                    l_name=last_name,
                    gender=gender,
                    dob=dob,
                    phone=phone_number,
                    address=address,
                    speciality=speciality,
                    experience=experience,


                )
                message = "Registration successful. You can now log in."
            elif role == 'patient':

                user = User.objects.create_user(
                    email=email,
                    password=password,
                    role='patient'
                )

                # Create Patient profile
                Patient.objects.create(
                    user=user,
                    f_name=first_name,
                    l_name=last_name,
                    gender=gender,
                    dob=dob,
                    phone=phone_number,
                    address=address,
                )
                message = "Registration successful. You can now log in."


    return render(request, 'signup.html', {'message': message})


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)  # Authenticate the user
        if user:
            login(request, user) # Log the user in and create a session
            if user.role == 'doctor':
                return redirect('doctor_profile', doctor_id=user.user_id)  # Redirect to the doctor's profile
            elif user.role == 'patient':
                return redirect('patient_dashboard')
            elif user.role == 'admin':
                return redirect('admin_dashboard')
        else:
            messages.error(request, "Invalid credentials.")


    return render(request, 'signin.html')


def articles(request):
    return render(request, 'articles.html')
@login_required(login_url='login')
def doctor_profile(request, doctor_id):
    try:
        doctor = Doctor.objects.get(user_id=doctor_id)
        clinics = Clinic.objects.filter(doctor=doctor)
    except Doctor.DoesNotExist:
        return render(request, '404.html', status=404)

    return render(request, 'd-profile.html', {'doctor': doctor, 'clinics': clinics})

def logoutUser(request):
    logout(request)
    return redirect('home')