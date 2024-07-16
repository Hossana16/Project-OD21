from django import forms
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView, UpdateView, CreateView, DetailView
from django.contrib import messages
from django.contrib.auth import logout
from allauth.account.views import SignupView, LoginView
from allauth.account.decorators import login_required 
from core.forms import AccountSignUpForm
from core.models import UserProfile, Education, SellerProfile, WorkExperience, Award, Skill
from .models import Service, Order, Review
from django.utils import timezone
from .forms import ReviewForm
from django.shortcuts import get_object_or_404, redirect
from .models import Job, JobApplication
from .forms import JobForm, JobApplicationForm, ServiceSearchForm, JobSearchForm
from core.forms import ServiceForm
# from decimal import Decimal  # Import Decimal if not already imported
import json
from django.shortcuts import render
from django.core.serializers.json import DjangoJSONEncoder
from .models import Service  # Adjust import according to your models file



# def service_map_view(request):
#     services = Service.objects.exclude(latitude=None).exclude(longitude=None)
    
#     # Convert Decimal fields to float for JSON serialization
#     services_data = json.dumps(list(services.values('title', 'description', 'latitude', 'longitude')), cls=DjangoJSONEncoder)
    
#     return render(request, 'map-view-test.html', {'services': services_data})


def service_map_view(request):
    services = Service.objects.exclude(latitude=None).exclude(longitude=None)
    
    # Convert Decimal fields to float for JSON serialization
    services_data = json.dumps(list(services.values('title', 'description', 'latitude', 'longitude')), cls=DjangoJSONEncoder)
    
    return render(request, 'map-view-test.html', {'services': services_data})


def maptest(request):
    template_name = 'map-test.html'
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            service = form.save(commit=False)
            service.latitude = request.POST.get('latitude')
            service.longitude = request.POST.get('longitude')
            
            # Get the seller profile of the logged-in user
            try:
                user_profile = request.user.userprofile.sellerprofile
                service.seller_profile = user_profile
            except Exception as e:
                messages.error(request, 'Error retrieving seller profile: ' + str(e))
                return render(request, template_name, {'form': form})
            
            service.save()
            messages.success(request, 'Service added successfully!')
            return redirect('core:manage-service')
    else:
        form = ServiceForm()
    
    return render(request, template_name, {'form': form})

# def service_map_view(request):
#     services = Service.objects.all()
#     service_data = [{
#         'title': service.title,
#         'description': service.description,
#         'latitude': service.latitude,
#         'longitude': service.longitude
#     } for service in services]

#     context = {
#         'services': service_data
#     }
#     return render(request, 'map-view-test.html', context)


class ServiceSearchView(ListView):
    model = Service
    # template_name = 'service_search_results.html'
    template_name = 'service/page-service.html'
    context_object_name = 'services'

    def get_queryset(self):
        query = self.request.GET.get('query')
        if query:
            return Service.objects.filter(title__icontains=query)
        return Service.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ServiceSearchForm()
        return context

class JobSearchView(ListView):
    model = Job
    # template_name = 'job_search_results.html'
    template_name = 'job/page-job-list.html'
    context_object_name = 'jobs'

    def get_queryset(self):
        query = self.request.GET.get('query')
        if query:
            return Job.objects.filter(title__icontains=query)
        return Job.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = JobSearchForm()
        return context


class AccountSignUpView(SignupView):
    form_class = AccountSignUpForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('core:home')

    success_url = reverse_lazy('core:home')

    def dispatch(self, request, *args, **kwargs):
        try:
            return super().dispatch(request, *args, **kwargs)
        except Exception as e:
            # Log the exception if needed
            print(f"Exception during registration: {e}")
            # Redirect to custom error page
            messages.error(request, "There was an issue with your registration. Please try again later.")
            return redirect('marketplace:login')

    def form_valid(self, form):
        response = super().form_valid(form)
        #log
        return response


class AccountSignInView(LoginView):
    template_name = 'accounts/login.html'
    success_url = reverse_lazy('core:dashboard')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(self.success_url)
        return super().dispatch(request, *args, **kwargs)


    def form_invalid(self, form):
        response = super().form_invalid(form)

        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')

        if self.request.user.is_authenticated:
            messages.success(self.request, 'Welcome back, {}'.format(username))
        else:
            messages.error(self.request, 'Invalid username or password. Please try again.')
        return response

@login_required
def Custom_logout(request):
    logout(request)
    messages.info(request, "Logged out successfully! ")
    return redirect('core:home')   


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = []  # We'll dynamically populate the fields later

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Populate the form fields based on the fields of the related User model
        for field in UserProfile._meta.get_fields():
            if field.name.startswith('user__'):
                self.fields[field.name.split('user__')[1]] = forms.CharField(
                    label=field.verbose_name,
                    initial=getattr(self.instance.user, field.name.split('user__')[1]),
                    required=False  # Adjust as needed
                )

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = UserProfile
    form_class = UserProfileForm
    template_name = 'dashboards/sellers-dashboard/profile.html'
    success_url = reverse_lazy('core:home')  # Set your desired success URL here

    def get_object(self, queryset=None):
        return self.request.user.userprofile

    def form_valid(self, form):
        # Save the form instance and return the response
        return super().form_valid(form)

class DashboardView(LoginRequiredMixin ,TemplateView):
    template_name = 'dashboards/sellers-dashboard/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
 

class ServiceView(TemplateView):
    template_name = 'service/page-service.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        services = Service.objects.all()
        # map_services = Service.objects.exclude(latitude=None).exclude(longitude=None)
        map_services = Service.objects.exclude(latitude=None).exclude(longitude=None)
    
        # Convert Decimal fields to float for JSON serialization
        services_data = json.dumps(list(map_services.values('title', 'description', 'latitude', 'longitude')), cls=DjangoJSONEncoder)
     
        # services_data = json.dumps(list(map_services.values('title', 'description', 'latitude', 'longitude')), cls=DjangoJSONEncoder)
    
        context['services'] = services_data
        context['service'] = services
        return context


class ServiceDetailsView(LoginRequiredMixin, DetailView):
    model = Service
    template_name = 'service/page-service-details.html'
    login_url = 'marketplace:login'

    def get_object(self):
        obj = super().get_object()
        obj.last_viewed = timezone.now()
        obj.save()
        return obj
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        service_reviews = Review.objects.filter(service=self.object)

        context['reviews'] = service_reviews
        context['total_reviews'] = service_reviews.count()
        context['form'] = ReviewForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        
        form = ReviewForm(request.POST)
        if form.is_valid():
            if not request.user.is_authenticated:
                return redirect('marketplace:login')
            review = form.save(commit=False)
            review.service = self.object
            review.buyer = request.user.userprofile  # Assuming UserProfile is linked to the User
            review.save()
            return redirect('marketplace:service-details', pk=self.object.pk)
        context = self.get_context_data()
        context['form'] = form
        return self.render_to_response(context)


class SellersView(TemplateView):
    template_name = 'seller/page-sellers.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        sellers = SellerProfile.objects.all()
        sellers_data = []

        for seller in sellers:
            services = Service.objects.filter(seller_profile=seller)
            reviews_count = Review.objects.filter(service__in=services).count()  # Get reviews count for services of the seller
            skills = seller.skills.all()[:3]  # Get up to 3 skills

            sellers_data.append({
                'seller': seller,
                'reviews_count': reviews_count,
                'skills': skills,
            })

        context['sellers_data'] = sellers_data
        return context


class SellersDetailsView(DetailView):
    model = SellerProfile
    template_name = 'seller/page-seller-details.html'
    
    
    def get_object(self):
        obj = super().get_object()
        obj.last_viewed = timezone.now()
        obj.save()
        return obj
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get the related educations for the current SellerProfile
        context['user_education'] = Education.objects.filter(user_profile=self.object)
        context['work_experiences'] = WorkExperience.objects.filter(user_profile=self.object)
        context['user_awards'] = Award.objects.filter(user_profile=self.object)
        context['skills'] = Skill.objects.filter(user_profile=self.object)
        services = Service.objects.filter(seller_profile=self.object)
        context['services'] = services

        total_reviews = Review.objects.filter(service__in=services).count()
        context['total_reviews'] = total_reviews
        return context
        

class JobListView(ListView):
    model = Job
    template_name = 'job/page-job-list.html'
    context_object_name = 'jobs'


class JobDetailView(DetailView):
    model = Job
    template_name = 'job/page-job-detail.html'
    context_object_name = 'job'

class JobApplicationView(LoginRequiredMixin, CreateView):
    model = JobApplication
    form_class = JobApplicationForm
    template_name = 'job/page-job-application.html'

    def form_valid(self, form):
       user_profile = self.request.user.userprofile
       form.instance.seller = get_object_or_404(SellerProfile, user_profile=user_profile)
       form.instance.job = get_object_or_404(Job, pk=self.kwargs['pk'])
       return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('marketplace:job-details', kwargs={'pk': self.kwargs['pk']})
    


def projects_main(request):
    template_name = 'page-project.html'
    return render(request, template_name)



def contact(request):
    template_name = 'contact.html'
    return render(request, template_name)
