from django.db import models

# Create your models here.
class Region(models.Model):

    name         = models.CharField(max_length=255)
    name_code    = models.CharField(max_length=255, default="")
    created_at   =  models.DateTimeField(auto_now_add=True)
    updated_at   =  models.DateTimeField(auto_now=True)


class Department(models.Model):

    name         = models.CharField(max_length=255)
    name_code    = models.CharField(max_length=255 , default="")
    region       = models.ForeignKey(Region , on_delete=models.CASCADE)
    created_at   =  models.DateTimeField(auto_now_add=True)
    updated_at   =  models.DateTimeField(auto_now=True)


class Arrondissement(models.Model):

    name         = models.CharField(max_length=255)
    name_code    = models.CharField(max_length=255, default="")
    department   = models.ForeignKey(Department , on_delete=models.CASCADE)
    created_at   =  models.DateTimeField(auto_now_add=True)
    updated_at   =  models.DateTimeField(auto_now=True)


