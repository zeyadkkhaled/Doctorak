from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

# Custom User Model
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # Hash password
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_staff", True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    role_choices = (
        ('doctor', 'Doctor'),
        ('patient', 'Patient'),
        ('admin', 'Admin'),
    )

    user_id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    password = models.TextField()
    role = models.CharField(max_length=10, choices=role_choices)

    # Required Django fields
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        db_table = 'user'
        managed = False  # Don't let Django manage this table


# Clinic Table
class Clinic(models.Model):
    clinic_id = models.AutoField(primary_key=True)
    clinic_name = models.CharField(max_length=100)
    address = models.TextField()
    country = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    region = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    working_hours = models.CharField(max_length=100)

    class Meta:
        db_table = 'clinic'
        managed = False


# Doctor Table
class Doctor(models.Model):
    doctor_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, db_column='user_id')
    profile_picture = models.ImageField(
        upload_to='static/images/doctors/profile_pics/',
        null=True,
        blank=True,
        default='static/images/defaults/default.png'
    )
    f_name = models.CharField(max_length=50)
    l_name = models.CharField(max_length=50)
    gender = models.CharField(max_length=10)
    dob = models.DateField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    speciality = models.CharField(max_length=100)
    experience = models.IntegerField()
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, db_column='clinic_id')

    class Meta:
        db_table = 'doctor'
        managed = False


# Patient Table
class Patient(models.Model):
    patient_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, db_column='user_id')
    profile_picture = models.ImageField(
        upload_to='static/images/patients/profile_pics/',
        null=True,
        blank=True,
        default='static/images/defaults/default.png'
    )
    f_name = models.CharField(max_length=50)
    l_name = models.CharField(max_length=50)
    gender = models.CharField(max_length=10)
    dob = models.DateField()
    phone = models.CharField(max_length=20)
    address = models.TextField()

    class Meta:
        db_table = 'patient'
        managed = False


# Admin Table
class Admin(models.Model):
    admin_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, db_column='user_id')
    f_name = models.CharField(max_length=50)
    l_name = models.CharField(max_length=50)
    gender = models.CharField(max_length=10)
    dob = models.DateField()
    phone = models.CharField(max_length=20)
    address = models.TextField()

    class Meta:
        db_table = 'admin'
        managed = False


# Appointment Table
class Appointment(models.Model):
    appointment_id = models.AutoField(primary_key=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, db_column='doctor_id')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, db_column='patient_id')
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, db_column='clinic_id')
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    status = models.CharField(max_length=20)

    class Meta:
        db_table = 'appointment'
        managed = False


# Medical Record Table
class MedicalRecord(models.Model):
    record_id = models.AutoField(primary_key=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True, db_column='doctor_id')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, db_column='patient_id')
    diagnosis = models.TextField()
    notes = models.TextField()
    treatment = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'medical_record'
        managed = False


# Prescription Table
class Prescription(models.Model):
    prescription_id = models.AutoField(primary_key=True)
    appointment = models.ForeignKey(Appointment, on_delete=models.SET_NULL, null=True, db_column='appointment_id')
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True, db_column='doctor_id')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, db_column='patient_id')
    medication = models.TextField()
    date_issued = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'prescription'
        managed = False


# Rating & Review Table
class RatingReview(models.Model):
    review_id = models.AutoField(primary_key=True)
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, db_column='appointment_id')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, db_column='doctor_id')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, db_column='patient_id')
    rating = models.SmallIntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()
    date_issued = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'rating_review'
        managed = False


# Weekly Availability Table
class WeeklyAvailability(models.Model):
    id = models.AutoField(primary_key=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, db_column='doctor_id')
    day_of_week = models.CharField(
        max_length=9,
        choices=[('Sunday', 'Sunday'), ('Monday', 'Monday'), ('Tuesday', 'Tuesday'),
                 ('Wednesday', 'Wednesday'), ('Thursday', 'Thursday'),
                 ('Friday', 'Friday'), ('Saturday', 'Saturday')]
    )
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        db_table = 'weekly_availability'
        managed = False
        unique_together = ('doctor', 'day_of_week')


# Availability Exception Table
class AvailabilityException(models.Model):
    id = models.AutoField(primary_key=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, db_column='doctor_id')
    date = models.DateField()
    is_available = models.BooleanField()
    override_start_time = models.TimeField(null=True)
    override_end_time = models.TimeField(null=True)

    class Meta:
        db_table = 'availability_exception'
        managed = False
        unique_together = ('doctor', 'date')
