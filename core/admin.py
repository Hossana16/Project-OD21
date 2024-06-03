from django.contrib import admin
from .models import User, UserProfile, SellerProfile, Education, WorkExperience, Award

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'is_superuser', 'gender', 'updated_at']
    

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['username', 'location', 'is_seller']
    list_editable = ['is_seller']


@admin.register(SellerProfile)
class SellerProfile(admin.ModelAdmin):
    list_display = ['username', 'bio', 'hourly_rate']

@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ['title', 'school_name', 'description', 'start_year', 'end_year']

@admin.register(WorkExperience)
class WorkExperience(admin.ModelAdmin):
    list_display = ['job_title', 'company_name', 'description', 'start_date', 'end_date']

@admin.register(Award)
class AwardAdmin(admin.ModelAdmin):
    list_display = ['title', 'issuer', 'description']

