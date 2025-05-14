# from email.utils import specialsre
from django.http import JsonResponse
from django.shortcuts import redirect
from .models import User, Doctor, Patient, Clinic, WeeklyAvailability, Appointment, AvailabilityException, MedicalRecord
from .models import MedicalHistory, RatingReview, Prescription,Admin
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from datetime import datetime, timedelta
from django.core.files.storage import FileSystemStorage
from django.utils import timezone


def home(request):
    login_url = reverse('login')
    # Calculate doctor counts per specialty
    specialty_counts = Doctor.objects.values('speciality').annotate(count=Count('speciality'))
    specialty_dict = {item['speciality']: item['count'] for item in specialty_counts}

    context = {
        'login_url': login_url,
        'specialty_counts': specialty_dict
    }
    return render(request, 'home.html', context)


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
                return redirect('admin_profile',admin_id=user.user_id)
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
        appointments = Appointment.objects.filter(doctor_id=doctor.doctor_id)
        reviews = RatingReview.objects.filter(doctor_id=doctor.doctor_id)

        # Debug prints
        print("Doctor ID:", doctor.doctor_id)
        print("Reviews:", reviews.values())

        return render(request, 'd-profile.html', {
            'doctor': doctor,
            'clinics': clinics,
            'weekly_availabilities': weekly_availabilities,
            'message': message,
            'exception_hours': exception_hours,
            'appointments': appointments,
            'reviews': reviews  # Changed from 'review' to 'reviews'
        })

    except Doctor.DoesNotExist:
        return render(request, '404.html', status=404)


@login_required(login_url='login')
def patient_profile(request, patient_id):
    message = request.GET.get('message')

    try:
        patient = Patient.objects.get(user_id=patient_id)
    except Patient.DoesNotExist:
        return render(request, '404.html', status=404)

    appointments = Appointment.objects.filter(patient_id=patient.patient_id)
    medical_record = MedicalRecord.objects.filter(patient_id=patient.patient_id)
    medical_history = MedicalHistory.objects.filter(patient_id=patient.patient_id).first()
    prescription = Prescription.objects.filter(patient_id=patient.patient_id)

    return render(request, 'p-profile.html', {
        'patient': patient,
        'appointments': appointments,
        'message': message,
        'medical_record': medical_record,
        'medicalhistory': medical_history,
        'prescription': prescription
    })


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


from django.contrib import messages
from datetime import datetime


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
        clinic.examination_price = request.POST.get('examination_price')
        clinic.save()

        # Handle weekly availability
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        WeeklyAvailability.objects.filter(doctor=doctor).delete()

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

        duplicate_found = False

        for date_str, start, end in zip(exception_dates, exception_starts, exception_ends):
            if date_str:
                date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()

                # Treat as off day if start or end is missing
                is_available = bool(start and end)
                start_time = start if start else None
                end_time = end if end else None

                # Check for duplicate
                if AvailabilityException.objects.filter(
                        doctor=doctor,
                        date=date_obj,
                        override_start_time=start_time,
                        override_end_time=end_time
                ).exists():
                    duplicate_found = True
                    continue  # Skip duplicate

                AvailabilityException.objects.create(
                    doctor=doctor,
                    date=date_obj,
                    is_available=is_available,
                    override_start_time=start_time,
                    override_end_time=end_time
                )

        msg = 'Clinic updated successfully.'
        if duplicate_found:
            msg += ' Note: Some duplicate exception days were skipped.'
        return redirect(f'/doctor/{doctor.user_id}?message={msg}')

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


from django.db.models import Q


def doctor_list(request):
    # Check if the user is authenticated
    if not request.user.is_authenticated:
        return redirect('login')
    patient = Patient.objects.get(user_id=request.user.user_id)
    # Get filters from request
    specialty = request.GET.get('specialty')
    search_query = request.GET.get('search')
    city = request.GET.get('city')
    region = request.GET.get('region')

    # Start with all doctors
    doctors = Doctor.objects.all()

    # Apply specialty filter if provided
    if specialty:
        from urllib.parse import unquote
        decoded_specialty = unquote(specialty)
        doctors = doctors.filter(speciality=decoded_specialty)

    # Apply search filter if provided
    if search_query:
        doctors = doctors.filter(
            Q(f_name__icontains=search_query) |
            Q(l_name__icontains=search_query) |
            Q(speciality__icontains=search_query) |
            Q(subspeciality__icontains=search_query)
        )

    # Apply location filters if provided
    if city:
        doctors = doctors.filter(clinic__city=city)
    if region:
        doctors = doctors.filter(clinic__region=region)

    context = {
        'patient': patient,
        'doctors': doctors,
        'specialty': specialty,
        'search_query': search_query,
        'city': city,
        'region': region
    }
    return render(request, 'spec.html', context)


@login_required(login_url='login')
def doctor_info(request, doctor_id):
    try:
        doctor = Doctor.objects.get(doctor_id=doctor_id)
        clinic = Clinic.objects.get(clinic_id=doctor.clinic_id)
        weekly_availabilities = WeeklyAvailability.objects.filter(doctor_id=doctor_id)
        exception_hours = AvailabilityException.objects.filter(doctor_id=doctor_id)
        reviews = RatingReview.objects.filter(doctor=doctor)
        reviews = RatingReview.objects.filter(doctor=doctor).select_related('patient').order_by('-date_issued')
        # Prepare availability data
        availability = []
        for day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']:
            avail = weekly_availabilities.filter(day_of_week=day).first()
            availability.append({
                'day_name': day,
                'available': bool(avail),
                'start_time': avail.start_time if avail else None,
                'end_time': avail.end_time if avail else None,
                'duration': 30  # Default duration (can be dynamic)
            })

        # Prepare exceptions
        exception_dates = []
        for ex in exception_hours:
            exception_dates.append({
                'date': ex.date,
                'available': ex.is_available,
                'start_time': ex.override_start_time,
                'end_time': ex.override_end_time
            })

        # Existing Appointments for frontend JS
        appointments = Appointment.objects.filter(doctor=doctor).values('appointment_date', 'appointment_time')

        # Handle booking POST
        if request.method == 'POST':
            selected_date = request.POST.get('date')
            selected_time_str = request.POST.get('time')
            notes = request.POST.get('notes')

            try:
                patient = Patient.objects.get(user=request.user)
            except Patient.DoesNotExist:
                return redirect('home')

            # Parse time
            selected_time = datetime.strptime(selected_time_str, "%H:%M").time()

            # Double booking check (30min buffer)
            min_time = (datetime.combine(datetime.today(), selected_time) - timedelta(minutes=30)).time()
            max_time = (datetime.combine(datetime.today(), selected_time) + timedelta(minutes=30)).time()

            overlapping = Appointment.objects.filter(
                doctor=doctor,
                appointment_date=selected_date,
                appointment_time__gte=min_time,
                appointment_time__lt=max_time
            )

            if overlapping.exists():
                return redirect(f'/doctor_info/{doctor_id}?message=Selected time is already booked.')

            # Save appointment
            Appointment.objects.create(
                doctor=doctor,
                patient=patient,
                clinic=clinic,
                appointment_date=selected_date,
                appointment_time=selected_time,
                status='Pending'
            )

            return redirect(f'/doctor_info/{doctor_id}?message=Appointment booked successfully.')

        context = {
            'doctor': doctor,
            'clinic': clinic,
            'availability': availability,
            'exception_dates': exception_dates,
            'reviews': reviews,
            'appointments': list(appointments),
            'message': request.GET.get('message', ''),
            'reviews': reviews,
        }

        return render(request, 'doctor_info.html', context)

    except Doctor.DoesNotExist:
        return render(request, '404.html', status=404)


@login_required(login_url='login')
def appointment_status(request, appointment_id):
    if request.method == 'POST':
        try:
            appointment = Appointment.objects.get(appointment_id=appointment_id)
            status = request.POST.get('status')
            if status:
                appointment.status = status
                appointment.save()
                return redirect(f'/doctor/{request.user.user_id}?message=Appointment {status.lower()} successfully.')
        except Appointment.DoesNotExist:
            return redirect(f'/doctor/{request.user.user_id}?message=Error updating appointment.')

    return redirect(f'/doctor/{request.user.user_id}')


@login_required(login_url='login')
def doctor_patient_view(request, patient_id):
    message = request.GET.get('message')
    patient = Patient.objects.get(user_id=patient_id)

    if not request.user.is_authenticated:
        return redirect('login')

    try:
        appointments = Appointment.objects.filter(patient_id=patient.patient_id)
    except Appointment.DoesNotExist:
        appointments = None
    try:
        medical_record = MedicalRecord.objects.filter(patient_id=patient.patient_id)
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

    return render(request, 'doctor_patient_view.html',
                  {'patient': patient, 'appointments': appointments, 'message': message,
                   'medicalhistory': medical_history, 'medical_record': medical_record})


@login_required(login_url='login')
def save_prescription(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == 'POST':
        appointment_id = request.POST.get('appointment_id')
        patient_id = request.POST.get('patient_id')
        doctor_id = request.POST.get('doctor_id')

        prescription = request.POST.get('prescription', '').strip()
        notes = request.POST.get('notes', '').strip()
        record_file = request.FILES.get('record_file')
        diagnosis = request.POST.get('diagnosis', '').strip()
        notes = request.POST.get('notes', '').strip()
        treatment = request.POST.get('treatment', '').strip()
        medication = request.POST.get('medication', '').strip()
        record_file = request.FILES.get('record_file')

        try:
            appointment = Appointment.objects.get(appointment_id=appointment_id)
            patient = Patient.objects.get(patient_id=patient_id)
            doctor = Doctor.objects.get(doctor_id=doctor_id)
        except (Appointment.DoesNotExist, Patient.DoesNotExist, Doctor.DoesNotExist):
            return redirect(request.META.get('HTTP_REFERER', '/'))

        # Save medical record
        record = MedicalRecord.objects.create(
            doctor=doctor,
            patient=patient,
            diagnosis=diagnosis,
            notes=notes,
            treatment=treatment
        )

        # Save uploaded file if present
        if record_file:
            import os
            upload_dir = 'static/medical_records/'
            os.makedirs(upload_dir, exist_ok=True)

            # Create a unique filename with timestamp
            timestamp = timezone.now().strftime('%Y%m%d_%H%M%S')
            filename = f'prescription_{patient.patient_id}_{timestamp}_{record_file.name}'
            file_path = os.path.join(upload_dir, filename)

            with open(file_path, 'wb+') as destination:
                for chunk in record_file.chunks():
                    destination.write(chunk)

            # Update the record with the file path
            record.file_path = file_path
            record.notes += f'\n[Attached file: {filename}]'
            record.save()
        else:
            record.save()

        # Save prescription
        Prescription.objects.create(
            appointment=appointment,
            doctor=doctor,
            patient=patient,
            medication=medication
        )

        return redirect(f'/doctor/{doctor.user.user_id}?message=Prescription saved')

    return redirect('/')


@login_required(login_url='login')
def save_review(request):
    if request.method == 'POST':
        appointment_id = request.POST.get('appointment_id')
        doctor_id = request.POST.get('doctor_id')
        patient_id = request.POST.get('patient_id')
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')

        try:
            appointment = Appointment.objects.get(appointment_id=appointment_id)
            doctor = Doctor.objects.get(doctor_id=doctor_id)
            patient = Patient.objects.get(patient_id=patient_id)

            # Create the review
            RatingReview.objects.create(
                appointment=appointment,
                doctor=doctor,
                patient=patient,
                rating=rating,
                comment=comment
            )

            return redirect(f'/patient/{patient.user.user_id}?message=Review submitted successfully.')
        except (Appointment.DoesNotExist, Doctor.DoesNotExist, Patient.DoesNotExist):
            return redirect(f'/patient/{request.user.user_id}?message=Error submitting review.')

    return redirect('home')


@login_required(login_url='login')
def admin_profile(request, admin_id):
    try:
        admin = Admin.objects.get(user_id=admin_id)
        doctors = Doctor.objects.all().select_related('user', 'clinic')
        patients = Patient.objects.all().select_related('user')
        appointments = Appointment.objects.all().select_related('doctor', 'patient', 'clinic')
        admins = Admin.objects.all().select_related('user')

        # Get counts for dashboard
        doctor_count = doctors.count()
        patient_count = patients.count()
        appointment_count = appointments.count()
        admin_count = admins.count()
        days=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        context = {
            'admin': admin,
            'doctors': doctors,
            'patients': patients,
            'appointments': appointments,
            'admins': admins,
            'doctor_count': doctor_count,
            'patient_count': patient_count,
            'appointment_count': appointment_count,
            'admin_count': admin_count,
            'days': days,
        }

        return render(request, 'admin_profile.html', context)

    except Admin.DoesNotExist:
        return render(request, '404.html', status=404)
def adminregister(request):
    if request.method == 'POST':
        first_name = request.POST['f_name']
        last_name = request.POST['l_name']
        email = request.POST['email']
        password = request.POST['password']
        gender = request.POST['gender']
        dob = request.POST['dob']
        phone_number = request.POST['phone']
        address = request.POST['address']
        role = 'admin'
        # Check if the email already exists
        if User.objects.filter(email=email).exists():
            return render(request, 'adminregister.html', {'message': "Email already exists."})
        else:
            user = User.objects.create_user(
                email=email,
                password=password,
                role='admin',
            )
            # Create an admin profile
            admin = Admin.objects.create(
                user=user,
                f_name=first_name,
                l_name=last_name,
                gender=gender,
                dob=dob,
                phone=phone_number,
                address=address
            )
            message = "Admin registration successful. You can now log in."
            return render(request, 'adminregister.html', {'message': message})
    return render(request, 'adminregister.html')


@login_required(login_url='login')
def edit_admin(request, admin_id):
    try:
        admin = Admin.objects.get(admin_id=admin_id)
        if request.method == 'POST':
            # Update admin profile
            admin.f_name = request.POST.get('f_name')
            admin.l_name = request.POST.get('l_name')
            admin.dob = request.POST.get('dob')
            admin.gender = request.POST.get('gender')
            admin.phone = request.POST.get('phone')
            admin.address = request.POST.get('address')

            # Update user email if changed
            user = admin.user
            new_email = request.POST.get('email')
            if user.email != new_email:
                if not User.objects.filter(email=new_email).exists():
                    user.email = new_email
                    user.save()
                else:
                    return JsonResponse({'success': False, 'message': 'Email already exists'})

            admin.save()
            return JsonResponse({'success': True, 'message': 'Admin updated successfully'})

        return JsonResponse({'success': False, 'message': 'Invalid request method'})

    except Admin.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Admin not found'})


@login_required(login_url='login')
def edit_doctor_admin(request, doctor_id):
    try:
        doctor = Doctor.objects.get(doctor_id=doctor_id)
        if request.method == 'POST':
            # Update doctor profile
            doctor.f_name = request.POST.get('f_name')
            doctor.l_name = request.POST.get('l_name')
            doctor.dob = request.POST.get('dob')
            doctor.gender = request.POST.get('gender')
            doctor.phone = request.POST.get('phone')
            doctor.address = request.POST.get('address')
            doctor.speciality = request.POST.get('speciality')
            doctor.experience = request.POST.get('experience')

            # Update clinic information
            clinic = doctor.clinic
            clinic.clinic_name = request.POST.get('clinic_name')
            clinic.phone = request.POST.get('clinic_phone')
            clinic.address = request.POST.get('clinic_address')
            clinic.country = request.POST.get('country')
            clinic.city = request.POST.get('city')
            clinic.region = request.POST.get('region')
            clinic.examination_price = request.POST.get('examination_price')
            clinic.save()

            # Update user email if changed
            user = doctor.user
            new_email = request.POST.get('email')
            if user.email != new_email:
                if not User.objects.filter(email=new_email).exists():
                    user.email = new_email
                    user.save()
                else:
                    return JsonResponse({'success': False, 'message': 'Email already exists'})

            doctor.save()
            return JsonResponse({'success': True, 'message': 'Doctor updated successfully'})

        return JsonResponse({'success': False, 'message': 'Invalid request method'})

    except Doctor.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Doctor not found'})


@login_required(login_url='login')
def edit_patient_admin(request, patient_id):
    try:
        patient = Patient.objects.get(patient_id=patient_id)
        if request.method == 'POST':
            # Update patient profile
            patient.f_name = request.POST.get('f_name')
            patient.l_name = request.POST.get('l_name')
            patient.dob = request.POST.get('dob')
            patient.gender = request.POST.get('gender')
            patient.phone = request.POST.get('phone')
            patient.address = request.POST.get('address')

            # Update user email if changed
            user = patient.user
            new_email = request.POST.get('email')
            if user.email != new_email:
                if not User.objects.filter(email=new_email).exists():
                    user.email = new_email
                    user.save()
                else:
                    return JsonResponse({'success': False, 'message': 'Email already exists'})

            patient.save()
            return JsonResponse({'success': True, 'message': 'Patient updated successfully'})

        return JsonResponse({'success': False, 'message': 'Invalid request method'})

    except Patient.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Patient not found'})


@login_required(login_url='login')
def edit_appointment_admin(request, appointment_id):
    try:
        appointment = Appointment.objects.get(appointment_id=appointment_id)
        if request.method == 'POST':
            # Update appointment
            doctor_id = request.POST.get('doctor_id')
            patient_id = request.POST.get('patient_id')
            appointment_date = request.POST.get('appointment_date')
            appointment_time = request.POST.get('appointment_time')
            status = request.POST.get('status')

            try:
                doctor = Doctor.objects.get(doctor_id=doctor_id)
                patient = Patient.objects.get(patient_id=patient_id)

                appointment.doctor = doctor
                appointment.patient = patient
                appointment.appointment_date = appointment_date
                appointment.appointment_time = appointment_time
                appointment.status = status
                appointment.save()

                return JsonResponse({'success': True, 'message': 'Appointment updated successfully'})

            except (Doctor.DoesNotExist, Patient.DoesNotExist):
                return JsonResponse({'success': False, 'message': 'Invalid doctor or patient ID'})

        return JsonResponse({'success': False, 'message': 'Invalid request method'})

    except Appointment.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Appointment not found'})