from django.db import models
from django.contrib.auth.hashers import make_password

class Admin(models.Model):
    adminName = models.CharField(max_length=100)
    adminEmail = models.EmailField(unique=True)
    adminRole = models.CharField(max_length=50)
    adminPassword = models.CharField(max_length=128)

    def save(self, *args, **kwargs):
        # Hash the password before saving
        # Removed password hashing here to avoid double/triple hashing
        super().save(*args, **kwargs)

    def __str__(self):
        return self.adminName

class Service(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Provider(models.Model):
    provider_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    location = models.CharField(max_length=100)
    availability = models.CharField(max_length=100)
    service = models.ForeignKey(Service, related_name='providers', on_delete=models.CASCADE)
    admin = models.ForeignKey('Admin', related_name='providers', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.provider_name} - {self.service.name}"

class Alert(models.Model):
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    message = models.TextField()
    public_date = models.DateTimeField()
    estate = models.CharField(max_length=100)  # e.g., Paradise Estate, Range View Estate, General
    role = models.CharField(max_length=50)  # e.g., residents, security
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.estate} - {self.role}"
