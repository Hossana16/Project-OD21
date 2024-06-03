from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),

    # manage service
    path('manage-service/', views.ManageServiceView.as_view(), name='manage-service'),
    path('manage-service/add/', views.AddServiceView.as_view(), name='add-service'),
    path('manage-service/edit/<int:pk>/', views.ServiceUpdateView.as_view(), name='edit-service'),

    # create & update profiles education level, workexperience, awards
    path('users/profile/', views.ProfileUpdateView.as_view(), name='profile'),
    path('users/education/', views.CreateEducation.as_view(), name='add-education'),
    path('users/workexperience/', views.CreateWorkExperience.as_view(), name='add-workexperience'),
    path('users/award/', views.CreateAward.as_view(), name='add-awards'),

    #reviews,  manage-job & manage-projects
    path('reviews/', views.ReviewsView.as_view(), name='reviews'),
    path('Manage-jobs/', views.ManageJobView.as_view(), name='manage-jobs'),
    path('Manage-projects/', views.ManageProjectView.as_view(), name='manage-projects'),

    # edit experiences
    path('edit/education/<int:pk>/', views.EducationUpdateView.as_view(), name='edit-education'),
    path('delete/education/<int:pk>/', views.EducationDeleteView.as_view(), name='delete-education'),
    path('edit/workexperience/<int:pk>', views.WorkExperienceUpdateView.as_view(), name='edit-workexperience'),
    path('edit/award/<int:pk>/', views.AwardUpdateView.as_view(), name='edit-awards'),
    
]