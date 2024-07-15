from allauth.account.forms import SignupForm, LoginForm
from django import forms
from .models import UserProfile, User
from django.contrib.auth.forms import UserChangeForm
from .models import User, UserProfile, SellerProfile, Education, WorkExperience, Award, Skill
from marketplace.models import Service

class AccountSignUpForm(SignupForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


    def save(self, request):
        user = super().save(request)
        user.is_buyer = True
        user.save()
        UserProfile.objects.create(user=user)
        return user    

class UserForm(UserChangeForm):
    password = None
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'phone_number', 'profile_image', 'date_of_birth', 'gender']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['location', 'language', 'language_level']

class SellerProfileForm(forms.ModelForm):
    class Meta:
        model = SellerProfile
        fields = ['profession', 'bio']

class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = ['start_year', 'end_year', 'title', 'school_name', 'description']

class WorkExperienceForm(forms.ModelForm):
    class Meta:
        model = WorkExperience
        fields = ['job_title', 'start_date', 'end_date', 'company_name', 'description']

class AwardForm(forms.ModelForm):
    class Meta:
        model = Award
        fields = ['title', 'issuer', 'date_awarded', 'description']

class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['title']

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['title', 'category', 'image', 'description', 'price', 'status', 'delivery_time']

