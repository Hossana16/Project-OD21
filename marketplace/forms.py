from django import forms
from .models import Review, Job, JobApplication

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'category', 'description', 'budget', 'status', 'image', 'job_type', 'end_at']

class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ['cover_letter']

class ServiceSearchForm(forms.Form):
    query = forms.CharField(label='Search Services', max_length=100)

class JobSearchForm(forms.Form):
    query = forms.CharField(label='Search Jobs', max_length=100)        
