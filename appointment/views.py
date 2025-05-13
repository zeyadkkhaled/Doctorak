# from email.utils import specialsre

from django.shortcuts import redirect
from .models import User, Doctor, Clinic, Patient, Clinic, WeeklyAvailability, Appointment, AvailabilityException,MedicalRecord
from .models import MedicalHistory
from django.shortcuts import render
from django.contrib.auth import authenticate, login, get_user_model, logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required


def home(request):
    login_url = reverse('login')
    return render(request, 'home.html', {'login_url': login_url})


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
        # For doctor only
        speciality = request.POST['speciality']
        experience = request.POST['experience']
        # For clinic only
        clinic_name = request.POST.get("clinic_name")
        clinic_phone = request.POST.get("clinic_phone")
        country = request.POST.get("country")
        city = request.POST.get("city")
        region = request.POST.get("region")

        # Check if the email already exists
        if User.objects.filter(email=email).exists():
            return render(request, 'signup1.html', {'message': "Email already exists."})
        else:
            if role == 'doctor':
                user = User.objects.create_user(
                    email=email,
                    password=password,
                    role='doctor',

                )

                # Create Clinic profile
                clinic = Clinic.objects.create(
                    clinic_name=clinic_name,
                    address=address,
                    phone=clinic_phone,
                    country=country,
                    city=city,
                    region=region,
                )

                # Create a Doctor profile
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
                    clinic=clinic,
                )

                # Create WeeklyAvailability profile
                # First get the selected working days and hours from the POST data
                selected_days = []
                for day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']:
                    start_time = request.POST.get(f'{day.lower()}_start')
                    end_time = request.POST.get(f'{day.lower()}_end')
                    print(f"Day: {day}, Start: {start_time}, End: {end_time}")  # Debug print
                    if start_time and end_time:
                        selected_days.append({
                            'day': day,
                            'start_time': start_time,
                            'end_time': end_time
                        })
                print("Selected days:", selected_days)  # Debug print
                # Create weekly availability entries for each selected day

                doctor = Doctor.objects.get(user=user)
                for day_data in selected_days:
                    try:
                        WeeklyAvailability.objects.create(
                            doctor=doctor,
                            day_of_week=day_data['day'],
                            start_time=day_data['start_time'],
                            end_time=day_data['end_time']
                        )
                        print(f"Created availability for {day_data['day']}")  # Debug print'
                        message = "Registration successful. You can now log in."
                    except Exception as e:
                        print(f"Error creating availability: {str(e)}")  # Debug print
            elif role == 'patient':

                user = User.objects.create_user(
                    email=email,
                    password=password,
                    role='patient'
                )

                # Create a Patient profile
                Patient.objects.create(
                    user=user,
                    f_name=first_name,
                    l_name=last_name,
                    gender=gender,
                    dob=dob,
                    phone=phone_number,
                    address=address,
                )
                # Create a MedicalHistory profile
                MedicalHistory.objects.create(
                    patient=user,
                    allergies="",
                    surgeries="",
                    past_illnesses="",
                    chronic_diseases="",
                    family_history="",
                    notes="",
                )
                message = "Registration successful. You can now log in."

    return render(request, 'signup1.html', {'message': message})


def loginPage(request):
    message = None
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)  # Authenticate the user
        if user:
            login(request, user)  # Log the user in and create a session
            if user.role == 'doctor':
                return redirect('doctor_profile', doctor_id=user.user_id)  # Redirect to the doctor's profile
            elif user.role == 'patient':
                return redirect('patient_profile', patient_id=user.user_id)
            elif user.role == 'admin':
                return redirect('admin_dashboard')
        else:
            message = "Invalid credentials."
    return render(request, 'signin.html', {'message': message})


def articles(request):
    return render(request, 'articles.html')


def logoutUser(request):
    logout(request)
    return redirect('home')


def profile_view(request):
    if not request.user.is_authenticated:
        return redirect('login')

    # Redirect to the appropriate profile page based on user role
    if hasattr(request.user, 'doctor'):
        return redirect('doctor_profile', doctor_id=request.user.user_id)
    else:
        return redirect('patient_profile', patient_id=request.user.user_id)


@login_required(login_url='login')
def doctor_profile(request, doctor_id):
    message = request.GET.get('message')
    try:
        doctor = Doctor.objects.get(user_id=doctor_id)
        clinics = Clinic.objects.get(clinic_id=doctor.clinic_id)
        weekly_availabilities = WeeklyAvailability.objects.filter(doctor_id=doctor.doctor_id)
        exception_hours = AvailabilityException.objects.filter(doctor_id=doctor.doctor_id)
    except Doctor.DoesNotExist:
        return render(request, '404.html', status=404)

    return render(request, 'd-profile.html',
                  {'doctor': doctor, 'clinics': clinics, 'weekly_availabilities': weekly_availabilities,
                   'message': message,'exception_hours': exception_hours})

@login_required(login_url='login')
def patient_profile(request, patient_id):
    message = request.GET.get('message')
    patient =Patient.objects.get(user_id=patient_id)

    if not request.user.is_authenticated:
        return redirect('login')

    try:
        appointments = Appointment.objects.filter(patient_id=patient.patient_id)
    except Appointment.DoesNotExist:
        appointments = None
    try:
        medical_record = MedicalRecord.objects.get(patient_id=patient.patient_id)
    except MedicalRecord.DoesNotExist:
        medical_record = None
    # Get the medical history for the patient
    try:
        medical_history = MedicalHistory.objects.get(patient_id=patient.patient_id)
    except MedicalHistory.DoesNotExist:
        medical_history = None
    # Check if the user is authenticated
    try:
        patient = Patient.objects.get(user_id=patient_id)
        appointments = Appointment.objects.filter(patient_id=patient.patient_id)
    except Patient.DoesNotExist:
        return render(request, '404.html', status=404)

    return render(request, 'p-profile.html', {'patient': patient, 'appointments': appointments, 'message': message,'medicalhistory': medical_history,'medical_record': medical_record})



@login_required(login_url='login')
def clinic_register(request):
    if request.method == 'POST':
        clinic_name = request.POST['clinic_name']
        address = request.POST['address']
        phone_number = request.POST['phone_number']
        doctor_id = request.POST['doctor_id']

        # Check if the clinic already exists
        if Clinic.objects.filter(clinic_name=clinic_name).exists():
            return render(request, 'clinic_register.html', {'message': "Clinic already exists."})
        else:
            # Create Clinic profile
            Clinic.objects.create(
                clinic_name=clinic_name,
                address=address,
                phone_number=phone_number,
                doctor_id=doctor_id
            )
            message = "Clinic registration successful."

    return render(request, 'clinic_register.html')
    message = None


@login_required(login_url='login')
def edit_doctor_profile(request, doctor_id):
    try:
        doctor = Doctor.objects.get(user_id=doctor_id)
        clinics = Clinic.objects.get(clinic_id=doctor.clinic_id)
        weekly_availabilities = WeeklyAvailability.objects.filter(doctor_id=doctor.doctor_id)
    except Doctor.DoesNotExist:
        return render(request, 'd-profile.html', {'message': "Doctor not found."})

    if request.method == 'POST':
        # Update doctor profile
        doctor.f_name = request.POST['first_name']
        doctor.l_name = request.POST['last_name']
        doctor.dob = request.POST['dob']
        doctor.gender = request.POST['gender']
        doctor.phone = request.POST['phone']
        doctor.address = request.POST['address']
        doctor.speciality = request.POST['speciality']
        doctor.experience = request.POST['experience']

        doctor.save()

        return redirect(f'/doctor/{doctor.user_id}?message=Profile updated successfully.')
    # If GET request
    else:
        return render(request, 'd-profile.html', {'doctor': doctor, 'clinics': clinics,
                                                  'weekly_availabilities': weekly_availabilities})


@login_required(login_url='login')
def edit_patient_profile(request, patient_id):
    try:
        patient = Patient.objects.get(user_id=patient_id)
    except Patient.DoesNotExist:
        return render(request, 'p-profile.html', {'message': "Patient not found."})
    if request.method == 'POST':
        # Update patient profile
        patient.f_name = request.POST['first_name']
        patient.l_name = request.POST['last_name']
        patient.dob = request.POST['dob']
        patient.gender = request.POST['gender']
        patient.phone = request.POST['phone']
        patient.address = request.POST['address']
        patient.save()
        return redirect(f'/patient/{patient.user_id}?message=Profile updated successfully.')
    # If GET request
    else:
        return render(request, 'p-profile.html', {'patient': patient})

@login_required(login_url='login')
def edit_clinic_profile(request, clinic_id):
    try:
        clinic = Clinic.objects.get(clinic_id=clinic_id)
        doctor = Doctor.objects.get(clinic_id=clinic_id)
    except (Clinic.DoesNotExist, Doctor.DoesNotExist):
        return redirect(f'/doctor/{doctor.user_id}?message=Clinic Does Not Exist.')

    if request.method == 'POST':
        # Update clinic basic info
        clinic.phone = request.POST.get('phone_number')
        clinic.country = request.POST.get('country')
        clinic.city = request.POST.get('city')
        clinic.region = request.POST.get('region')
        clinic.address = request.POST.get('address')
        clinic.save()

        # Handle weekly availability
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

        # First, clear existing weekly availability
        WeeklyAvailability.objects.filter(doctor=doctor).delete()

        # Add new weekly availability
        for day in days:
            start_time = request.POST.get(f'{day}_start')
            end_time = request.POST.get(f'{day}_end')
            if start_time and end_time:
                WeeklyAvailability.objects.create(
                    doctor=doctor,
                    day_of_week=day.capitalize(),
                    start_time=start_time,
                    end_time=end_time
                )

        # Handle exception days
        exception_dates = request.POST.getlist('new_exception_date')
        exception_starts = request.POST.getlist('new_exception_start')
        exception_ends = request.POST.getlist('new_exception_end')

        # Clear existing exceptions
        AvailabilityException.objects.filter(doctor=doctor).delete()

        # Add new exceptions
        for date, start, end in zip(exception_dates, exception_starts, exception_ends):
            if date:  # Only process if there's a date
                AvailabilityException.objects.create(
                    doctor=doctor,
                    date=date,
                    is_available=bool(start and end),  # If both times exist, day is available
                    override_start_time=start if start else None,
                    override_end_time=end if end else None
                )

        return redirect(f'/doctor/{doctor.user_id}?message=Clinic updated successfully.')

    # If GET request, render the form with current data
    context = {
        'doctor': doctor,
        'clinics': clinic,
        'weekly_availabilities': WeeklyAvailability.objects.filter(doctor=doctor),
        'exception_hours': AvailabilityException.objects.filter(doctor=doctor),
    }
    return render(request, 'd-profile.html', context)

@login_required(login_url='login')
def edit_exception_hours(request, exception_id):

    try:
        exception_hours = AvailabilityException.objects.get(id=exception_id)
        doctor_id = exception_hours.doctor_id
        doctor = Doctor.objects.get(doctor_id=doctor_id)
        user_id = doctor.user_id
    except AvailabilityException.DoesNotExist:
        return redirect('home')

    if request.method == 'POST':
        exception_hours.delete()
        return redirect(f'/doctor/{user_id}?message=Exception day deleted successfully.')
    return redirect('home')  # redirect if accessed via GET


@login_required(login_url='login')
def change_profile_picture(request):
    if request.method == 'POST' and request.FILES.get('profile_picture'):
        user = request.user
        image = request.FILES['profile_picture']

        try:
            if user.role == 'doctor':
                profile = Doctor.objects.get(user=user)
                upload_path = f'static/images/doctors/profile_pics/{user.user_id}.png'
            else:
                profile = Patient.objects.get(user=user)
                upload_path = f'static/images/patients/profile_pics/{user.user_id}.png'

            # Delete old picture if exists
            import os
            if os.path.exists(upload_path):
                os.remove(upload_path)

            # Save new picture
            with open(upload_path, 'wb+') as destination:
                for chunk in image.chunks():
                    destination.write(chunk)

            # Update profile picture path in database
            if user.role == 'doctor':
                Doctor.objects.filter(user=user).update(profile_picture=upload_path)
                return redirect(f'/doctor/{user.user_id}?message=Profile picture updated successfully.')
            else:
                Patient.objects.filter(user=user).update(profile_picture=upload_path)
                return redirect(f'/patient/{user.user_id}?message=Profile picture updated successfully.')

        except (Doctor.DoesNotExist, Patient.DoesNotExist) as e:
            return redirect('home')

    return redirect('home')

@login_required(login_url='login')
def edit_medical_history(request, patient_id):
    patient = Patient.objects.get(user_id=patient_id)

    if not request.user.is_authenticated:
        return redirect('login')

    try:
        medical_history = MedicalHistory.objects.get(patient=patient)
    except MedicalHistory.DoesNotExist:
        MedicalHistory.objects.create(
            patient=patient,
            allergies="",
            surgeries="",
            past_illnesses="",
            chronic_diseases="",
            family_history="",
            notes="",
        )

    if request.method == 'POST':
        allergies = request.POST.get('allergies')
        surgeries = request.POST.get('surgeries')
        past_illnesses = request.POST.get('past_illnesses')
        chronic_diseases = request.POST.get('chronic_diseases')
        family_history = request.POST.get('family_history')
        notes = request.POST.get('notes')

        # Update the medical history
        MedicalHistory.objects.filter(patient=patient).update(
            allergies=allergies,
            surgeries=surgeries,
            past_illnesses=past_illnesses,
            chronic_diseases=chronic_diseases,
            family_history=family_history,
            notes=notes
        )

        return redirect(f'/patient/{patient_id}?message=Medical history updated successfully.')

    return redirect(f'/patient/{patient_id}?message=Failed to update medical history.')
