from django.urls import path
from . import views

urlpatterns=[
    path('', views.placement, name='placement'),
    path('newJobs', views.newJobs, name='newJobs'),
    path('savedCompany', views.savedCompany, name='savedCompany'),
    path('allCompany', views.allCompany, name='allCompany'),
    path('addNew', views.addNew, name='addNew'),
    
    path('addCompany', views.addCompany, name='addCompany'),
    path('addSalary', views.addSalary, name='addSalary'),
    path('addJob', views.addJob, name='addJob'),
    path('addSavedCompany', views.addSavedCompany, name='addSavedCompany'),

    path('getAllCompany', views.getAllCompany, name='getAllCompany'),
    path('getSavedCompany', views.getSavedCompany, name='getSavedCompany'),
    path('getSalary', views.getSalary, name='getSalary'),
    path('getJobData', views.getJobData, name='getJobData'),

    path('updateDatetime', views.updateDatetime, name='updateDatetime'),

]