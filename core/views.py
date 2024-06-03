from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import UserProfile, Education, WorkExperience, Award
from .forms import UserForm, UserProfileForm, SellerProfileForm, EducationForm, WorkExperienceForm, AwardForm, ServiceForm
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, ListView, CreateView, DetailView
from django.views.generic.edit import UpdateView, DeleteView 
from django.contrib import messages
from django.db.models import Sum, Count
from django.contrib.auth import logout
from allauth.account.views import SignupView, LoginView
from allauth.account.decorators import login_required 
from core.forms import AccountSignUpForm
from core.models import UserProfile, SellerProfile
from marketplace.models import Service, Review, Job, JobApplication
from marketplace.forms import JobForm


class HomeView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        services = Service.objects.all()

        context['services'] = services
        return context   


class DashboardView(LoginRequiredMixin ,TemplateView):
    template_name = 'dashboards/sellers-dashboard/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        total_number_of_service = Service.objects.all().count()

        context['total_number_of_service'] = total_number_of_service
        return context
    
    # def dispatch(self, request, *args, **kwargs):
    #     if not hasattr(request.user, 'adminprofile'):
    #         return redirect(reverse('inventory:sales-list'))
        
    #     return super().dispatch(request, *args, **kwargs)



class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = UserProfile
    form_class = UserProfileForm
    template_name = 'dashboards/sellers-dashboard/profile.html'
    success_url = reverse_lazy('core:profile')
    
    def get_object(self, queryset=None):
        return get_object_or_404(UserProfile, user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_profile = self.get_object()
        seller_profile = user_profile.sellerprofile 
        user_education = Education.objects.filter(user_profile=seller_profile)
        user_workexperience = WorkExperience.objects.filter(user_profile=seller_profile)
        user_awards = Award.objects.filter(user_profile=seller_profile)
        context['user_form'] = UserForm(instance=self.request.user)
        context['sellerprofile_form'] = SellerProfileForm(instance=self.request.user)
        context['profile_form'] = self.get_form()
        context['user_education'] = user_education  
        context['work_experiences'] = user_workexperience  
        context['user_awards'] = user_awards
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        user_form = UserForm(request.POST, request.FILES, instance=request.user)
        sellerprofile_form = SellerProfileForm(request.POST, request.FILES, instance=request.user)
        profile_form = self.get_form()

        if user_form.is_valid() and profile_form.is_valid() and sellerprofile_form.is_valid():
            return self.forms_valid(user_form, profile_form, sellerprofile_form)
        else:
            return self.forms_invalid(user_form, profile_form, sellerprofile_form)

    def forms_valid(self, user_form, sellerprofile_form, profile_form):
        user_form.save()
        sellerprofile_form.save()
        profile_form.save()
        messages.success(self.request, 'Profile updated successfully.')
        return super().form_valid(profile_form)
    
    def forms_invalid(self, user_form, sellerprofile_form, profile_form):
        messages.error(self.request, 'Failed to update the profile. Please check the form for errors.')
        return self.render_to_response(self.get_context_data(user_form=user_form, sellerprofile_form=sellerprofile_form, profile_form=profile_form))


# organize and Manage
class ManageServiceView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboards/sellers-dashboard/manage-service/manage-service.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        seller_profile = SellerProfile.objects.get(user_profile__user=self.request.user)
        services = Service.objects.filter(seller_profile=seller_profile)
        context['services'] = services
        return context
    
    # def dispatch(self, request, *args, **kwargs):
    #     if not hasattr(request.user, 'sellerprofile'):
    #         return redirect(reverse('core:dashboard'))
        
        # return super().dispatch(request, *args, **kwargs)

class ReviewsView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboards/sellers-dashboard/page-dashboard-reviews.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        seller_profile = SellerProfile.objects.get(user_profile__user=self.request.user)
        # Fetching services related to the seller
        services = Service.objects.filter(seller_profile=seller_profile)
        # Fetching reviews related to those services
        reviews = Review.objects.filter(service__in=services)
        context['reviews'] = reviews
        return context
    
# manage Jobs     
class ManageJobView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboards/sellers-dashboard/manage-jobs/page-dashboard-manage-jobs.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        userprofile = UserProfile.objects.get(user=self.request.user)
        jobs = Job.objects.filter(user=userprofile)
        
        # dictionary  holds job applications count for each job
        job_applications_count = {job: JobApplication.objects.filter(job=job).count() for job in jobs}
        
        context['job_applications_count'] = job_applications_count
        context['jobs'] = jobs
        return context


class JobCreateView(LoginRequiredMixin, CreateView):
    model = Job
    form_class = JobForm
    template_name = 'dashboards/sellers-dashboard/manage-jobs/add-job.html'
    success_url = reverse_lazy('core:manage-jobs')

    def form_valid(self, form):
        user_profile = self.request.user.userprofile
        # form.instance.user_profile = user_profile
        form.instance.user = user_profile
        return super().form_valid(form)


class JobUpdateView(LoginRequiredMixin, UpdateView):
    model = Job
    fields = ['title', 'category', 'image', 'description', 'budget', 'status', 'image', 'job_type', 'end_at']
    template_name = 'dashboards/sellers-dashboard/manage-jobs/edit-job.html'
    success_url = reverse_lazy('core:manage-jobs')
    context_object_name = 'job'

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        return context   
    
class JobDeleteView(LoginRequiredMixin, DeleteView):
    model = Job
    success_url = reverse_lazy('core:manage-jobs')
    template_name = 'dashboards/sellers-dashboard/manage-jobs/confirm-delete-job.html'

    def get_object(self, queryset=None):
        obj = get_object_or_404(Job, pk=self.kwargs['pk'])
        return obj     


class ManageProjectView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboards/sellers-dashboard/page-dashboard-manage-projects.html'



class CreateEducation(LoginRequiredMixin, CreateView):
    model = Education
    form_class = EducationForm
    template_name = 'dashboards/sellers-dashboard/add-education.html'
    success_url = reverse_lazy('core:profile')
    
    def form_valid(self, form):
        user_profile = self.request.user.userprofile.sellerprofile
        form.instance.user_profile = user_profile
        response =  super().form_valid(form)
            
        messages.success(self.request, 'Education Added successfully!')
        return response
    
class AddServiceView(LoginRequiredMixin, CreateView):
    model = Service
    form_class = ServiceForm
    template_name = 'dashboards/sellers-dashboard/manage-service/add-service.html'
    success_url = reverse_lazy('core:manage-service')
    
    def form_valid(self, form):
        user_profile = self.request.user.userprofile.sellerprofile
        form.instance.seller_profile = user_profile
        response =  super().form_valid(form)
            
        messages.success(self.request, 'Service Added successfully!')
        return response

class ServiceUpdateView(LoginRequiredMixin, UpdateView):
    model = Service
    fields = ['title', 'category', 'image', 'description', 'price', 'status', 'delivery_time']
    template_name = 'dashboards/sellers-dashboard/manage-service/edit-service.html'
    success_url = reverse_lazy('core:manage-service')
    context_object_name = 'service'

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        return context    


class ServiceDeleteView(LoginRequiredMixin, DeleteView):
    model = Service
    success_url = reverse_lazy('core:manage-service')
    template_name = 'dashboards/sellers-dashboard/manage-service/confirm-delete-service.html'

    def get_object(self, queryset=None):
        obj = get_object_or_404(Service, pk=self.kwargs['pk'])
        return obj

# creating and editing profile 
class CreateEducation(LoginRequiredMixin, CreateView):
    model = Education
    form_class = EducationForm
    template_name = 'dashboards/sellers-dashboard/add-education.html'
    success_url = reverse_lazy('core:profile')
    
    def form_valid(self, form):
        user_profile = self.request.user.userprofile.sellerprofile
        form.instance.user_profile = user_profile
        response =  super().form_valid(form)
            
        messages.success(self.request, 'Education Added successfully!')
        return response

class EducationDeleteView(LoginRequiredMixin, DeleteView):
    model = Education
    success_url = reverse_lazy('core:profile')
    template_name = 'confirm_delete_education.html'  # Ensure this template exists

    def get_object(self, queryset=None):
        obj = get_object_or_404(Education, pk=self.kwargs['pk'], user_profile__user=self.request.user)
        return obj


# def delete_education(request, education_id):
#     education = get_object_or_404(Education, pk=education_id, user=request.user)
#     if request.method == 'POST':
#         education.delete()
#         return redirect('core:profile')
#     return render(request, 'confirm_delete_education.html', {'education': education})    

class CreateWorkExperience(LoginRequiredMixin, CreateView):
    model = WorkExperience
    form_class = WorkExperienceForm
    template_name = 'dashboards/sellers-dashboard/add-workexperience.html'
    success_url = reverse_lazy('core:profile')

    def form_valid(self, form):
        user_profile = self.request.user.userprofile.sellerprofile
        form.instance.user_profile = user_profile
        response =  super().form_valid(form)
            
        messages.success(self.request, 'Workexperience Was Added successfully!')
        return response
    
class CreateAward(LoginRequiredMixin, CreateView):
    model = Award
    form_class = AwardForm
    template_name = 'dashboards/sellers-dashboard/add-award.html'
    success_url = reverse_lazy('core:profile')
    
    def form_valid(self, form):
        user_profile = self.request.user.userprofile.sellerprofile
        form.instance.user_profile = user_profile
        response =  super().form_valid(form)
            
        messages.success(self.request, 'Award Was Added successfully!')
        return response
    

# editing
class EducationUpdateView(LoginRequiredMixin, UpdateView):
    model = Education
    fields = ['start_year', 'end_year', 'title', 'school_name', 'description']
    template_name = 'dashboards/sellers-dashboard/edit/edit-education.html'
    success_url = reverse_lazy('core:profile')
    context_object_name = 'education'

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        return context     

class WorkExperienceUpdateView(LoginRequiredMixin, UpdateView):
    model = WorkExperience
    fields = ['job_title', 'start_date', 'end_date', 'company_name', 'description']
    template_name = 'dashboards/sellers-dashboard/edit/edit-workexperience.html'
    success_url = reverse_lazy('core:profile')
    context_object_name = 'workexperience'

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        return context     
    
class AwardUpdateView(LoginRequiredMixin, UpdateView):
    model = Award
    fields = ['title', 'date_awarded', 'issuer', 'description',]
    template_name = 'dashboards/sellers-dashboard/edit/edit-award.html'
    success_url = reverse_lazy('core:profile')
    context_object_name = 'award'

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        return context     



@login_required
def Custom_logout(request):
    logout(request)
    messages.info(request, "Logged out successfully! ")
    return redirect('core:home')   
