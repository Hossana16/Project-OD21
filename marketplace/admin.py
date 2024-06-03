from django.contrib import admin
from .models import ServiceCategory, Service, Order, Review, Job, JobCategory, JobApplication


@admin.register(ServiceCategory)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'status', 'delivery_time', 'created_at']
    list_editable= ['status']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['buyer', 'service', 'status', 'order_date', 'delivery_date']
    list_editable = ['status']

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display= ['service', 'buyer', 'comment', 'created_at']


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display= ['title', 'category', 'budget', 'created_at']

@admin.register(JobCategory)
class JobCategoryAdmin(admin.ModelAdmin):
    list_display= ['name']

@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display= ['cover_letter','created_at']


# # admin.site.register(Category)
# admin.site.register(Service)
# admin.site.register(Order)
# admin.site.register(Review)
