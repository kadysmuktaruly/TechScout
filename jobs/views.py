from django.shortcuts import render
from django.http import HttpResponse, Http404
from .models import Job
# Create your views here.

def home(request):
    return render(request, 'myapp/home.html')

def job_list(request):
    jobs = Job.objects.all()  # get all jobs
    return render(request, "jobs/job_list.html", {"jobs": jobs})

def job_detail(request, job_id):
    return HttpResponse(f"Job detail {job_id}")

def job_create(request):
    return HttpResponse("Create job")

def job_update(request, job_id):
    return HttpResponse(f"Update job {job_id}")

def job_delete(request, job_id):
    return HttpResponse(f"Delete job {job_id}")
