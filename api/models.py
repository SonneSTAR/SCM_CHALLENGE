from email.policy import default
from enum import unique
from unittest.util import _MAX_LENGTH
from uuid import uuid4
from django.db import models

# Create your models here.

class Company(models.Model):
    id =  models.BigAutoField(auto_created=False, primary_key=True, serialize=False, verbose_name='ID')
    name= models.CharField(max_length=50, default="", null= True)
    website= models.URLField(max_length=100, null = True, blank = True)
    foundation = models.PositiveIntegerField(null= True)

    def __str__(self):
        return self.name
    
#UNO(compañias) A MUCHOS(empleados)
class Employee(models.Model):
    id =  models.BigAutoField(auto_created=False, primary_key=True, serialize=False, verbose_name='ID')
    name= models.CharField(max_length=50, default="")
    company = models.ForeignKey(Company, null= True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.id

class Enrollment(models.Model):
    id =  models.BigAutoField(auto_created=False, primary_key=True, serialize=False, verbose_name='ID')
    photo = models.ImageField(null= True, blank= True) 
    employee = models.ForeignKey(Employee, null= True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.id