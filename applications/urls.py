from django.urls import path
from . import views
from applications.views import application_create

urlpatterns = [
    path('create/<int:job_id>/', application_create, name='application_create'),
    # Add other application-related URLs here if needed
]