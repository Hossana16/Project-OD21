from django.urls import path
from . import views
from core.urls import views as core

app_name ='marketplace'

urlpatterns = [
    # test urls
    path('search/services/', views.ServiceSearchView.as_view(), name='service_search'),
    path('search/jobs/', views.JobSearchView.as_view(), name='job_search'),
    # path('', core.home),
    path('register/', views.AccountSignUpView.as_view(), name='register'),
    path('login/', views.AccountSignInView.as_view(), name='login'),
    path('logout/', views.Custom_logout, name='logout'),
    # services urls
    path('services/', views.ServiceView.as_view(), name='services-main'),
    path('service/details/<int:pk>/', views.ServiceDetailsView.as_view(), name='service-details'),
    path('projects/', views.projects_main, name='projects'),
    # jobs
    path('jobs/', views.JobListView.as_view(), name='jobs'),
    path('job-detail/<int:pk>', views.JobDetailView.as_view(), name='job-details'),
    path('job-application/<int:pk>', views.JobApplicationView.as_view(), name='job-application'),
    # sellers urls
    path('Sellers/', views.SellersView.as_view(), name='sellers'),
    path('sellers/details/<int:pk>/', views.SellersDetailsView.as_view(), name='seller-details'),

    path('contact/', views.contact, name='contact'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    # path('profile/', views.ProfileUpdateView.as_view(), name='profile'),
    path('contact/', views.contact, name='contact'),

]