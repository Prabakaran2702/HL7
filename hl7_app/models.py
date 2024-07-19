from django.db import models

# Create your models here.

class Patient(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    mrn = models.CharField(max_length=100)
    physician_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)

class EncounterCharges(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    charges = models.DecimalField(max_digits=10, decimal_places=2)

class ErrorCharges(models.Model):
    error_type = models.CharField(max_length=255)
    error_message = models.TextField()
    mrn = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)  