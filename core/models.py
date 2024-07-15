from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from PIL import Image

class User(AbstractUser):
    email = models.EmailField(unique=True, max_length=250)
    phone_number = models.CharField(max_length=10, help_text='example 0743000000')
    date_joined = models.DateTimeField(default=timezone.now)
    date_of_birth = models.DateField(null=True, blank=True, help_text='2000-05-18')
    is_buyer = models.BooleanField(default=False)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], blank=True)
    profile_image = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        if self.profile_image:
            img = Image.open(self.profile_image.path)
            if img.height > 50 or img.width > 50:
                output_size = (50, 50)
                img.thumbnail(output_size)
                img.save(self.profile_image.path)
  
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_seller = models.BooleanField(default=True)
    location = models.CharField(max_length=80)
    language = models.CharField(max_length=100, blank=True)
    language_level = models.CharField(max_length=100, blank=True)

    def username(self):
        return self.user.username

    def __str__(self):
        return self.user.username

class SellerProfile(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    profession = models.CharField(max_length=255)
    bio = models.CharField(max_length=100)
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def username(self):
        return self.user_profile.user.username

    def __str__(self):
        return self.user_profile.user.username + "'s Seller Profile"
    

class Education(models.Model):
    user_profile = models.ForeignKey(SellerProfile, on_delete=models.CASCADE, related_name='educations')
    start_year = models.IntegerField()
    end_year = models.IntegerField()
    title = models.CharField(max_length=200)
    school_name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.title} at {self.school_name}'

class WorkExperience(models.Model):
    user_profile = models.ForeignKey(SellerProfile, on_delete=models.CASCADE, related_name='work_experiences')
    job_title = models.CharField(max_length=200)
    start_date = models.DateField(help_text='2021-05-18')
    end_date = models.DateField(blank=True, null=True)
    company_name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.job_title} at {self.company_name}'

class Award(models.Model):
    user_profile = models.ForeignKey(SellerProfile, on_delete=models.CASCADE, related_name='awards')
    title = models.CharField(max_length=200)
    issuer = models.CharField(max_length=200)
    date_awarded = models.DateField(help_text='2024-05-18')
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.title} from {self.issuer}'    

class Skill(models.Model):
    user_profile = models.ForeignKey(SellerProfile, on_delete=models.CASCADE, related_name='skills')
    title = models.CharField(max_length=200, unique=True)