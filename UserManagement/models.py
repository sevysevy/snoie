from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class OrganisationType(models.Model):

    name      = models.CharField(max_length=255)
    name_code = models.CharField(max_length= 255)
    created_at   =  models.DateTimeField(auto_now_add=True)
    updated_at   =  models.DateTimeField(auto_now=True)


class Organisation(models.Model):
    
    name = models.CharField(max_length=255)
    num_enreg = models.CharField(max_length=100)
    email    = models.EmailField(max_length=255)
    phone    = models.CharField(max_length=255)
    domaine    = models.CharField(max_length=255)
    logo       = models.CharField(max_length=255)
    organisation_type   = models.ForeignKey(OrganisationType , on_delete=models.SET_NULL, null=True)
    desc_org     = models.TextField()
    isArchive    =  models.BooleanField()
    created_at   =  models.DateTimeField(auto_now_add=True)
    updated_at   =  models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    

class Role(models.Model):
    
    name = models.CharField(max_length=255)
    name_code = models.CharField(max_length=255)
    desc_role     = models.TextField()
    created_at   =  models.DateTimeField(auto_now_add=True)
    updated_at   =  models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name



class UserProfile(models.Model):
   
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    firstName = models.CharField(max_length=255 , blank=True)
    lastName  = models.CharField(max_length=255, blank=True)
    fullName = models.CharField(max_length=255)
    email    = models.EmailField(max_length=255)
    phone    = models.CharField(max_length=255, null=True)
    active   =  models.BooleanField(default=True)
    organisation = models.ForeignKey(Organisation , on_delete=models.SET_NULL, null=True)
    isArchive    =  models.BooleanField( default=False)
    role         =  models.ForeignKey(Role , on_delete=models.SET_NULL, null=True)
    created_at   =  models.DateTimeField(auto_now_add=True)
    updated_at   =  models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username
    

    def is_observator(self):

        return self.role.name_code == 'observator'
    
    def is_admin(self):

        return self.role.name_code == 'admin'
    
    def is_reponsible(self):

        return self.role.name_code == 'responsable'
    
    def is_consultant(self):

        return self.role.name_code == 'consultant'

    def is_coordonator(self):

        return self.role.name_code == 'coordonator'
    
    def is_abonne(self):

        return self.role.name_code == 'abonne'
    

