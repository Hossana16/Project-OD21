from django.db import models
from django.conf import settings
from core.models import SellerProfile, UserProfile
from PIL import Image

class ServiceCategory(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Service(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('pending', 'Pending'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    ]

    seller_profile = models.ForeignKey(SellerProfile, on_delete=models.CASCADE, related_name='services')
    category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE, related_name='services')
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='services_images/', blank=True, null=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    delivery_time = models.DurationField(help_text='Delivery time in days')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    service_location = models.CharField(max_length=255, null=True, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        if self.image:
            img = Image.open(self.image.path)
            if img.height > 329 or img.width > 245:
                output_size = (329, 245)
                img.thumbnail(output_size)
                img.save(self.image.path)

    def review_count(self):
        return self.reviews.count()
        
    def delete(self, *args, **kwargs):
        self.image.delete()   
        super().delete(*args, **kwargs)             

    def __str__(self):
        return self.title
    

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    ]
    
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='orders')
    buyer = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='orders')
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    delivery_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f'Order #{self.id} for {self.service.title} by {self.buyer.user.username}'

class Review(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='reviews')
    buyer = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField()
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Review for {self.service.title} by {self.buyer.user.username}'


class JobCategory(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Job(models.Model):
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('closed', 'Closed'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]
    JOB_CHOICES = [
        ('Freelance', 'Freelance'),
        ('Full time', 'Full time'),
        ('Part time', 'Part time'),
        ('Internship', 'Internship'),
    ]

    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='jobs')
    title = models.CharField(max_length=255)
    category = models.ForeignKey(JobCategory, on_delete=models.CASCADE, related_name='services')
    description = models.TextField()
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='open')
    image = models.ImageField(upload_to='Jobs_images/', blank=True, null=True)
    job_type = models.CharField(max_length=15, choices=JOB_CHOICES, default='Full time')
    created_at = models.DateTimeField(auto_now_add=True)
    end_at = models.DateTimeField(null=True, blank=True, help_text='set the end date of the applications')
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        if self.image:
            img = Image.open(self.image.path)
            if img.height > 329 or img.width > 245:
                output_size = (60, 60)
                img.thumbnail(output_size)
                img.save(self.image.path)


    def __str__(self):
        return self.title            
    


class JobApplication(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    seller = models.ForeignKey(SellerProfile, on_delete=models.CASCADE, related_name='applications')
    cover_letter = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.seller.user_profile.user.username} applied for {self.job.title}'    