from django.shortcuts import render
from django.http import HttpResponse, Http404
from .models import Job
from .forms import JobForm


def home(request):
    return render(request, 'jobs/home.html')

def job_list(request):
    jobs = Job.objects.all()

    
    location = request.GET.get("location")
    keyword = request.GET.get("q")
    remote = request.GET.get("remote")

    if location:
        jobs = jobs.filter(location__icontains=location)
    if keyword:
        jobs = jobs.filter(
            title__icontains=keyword
        ) | jobs.filter(
            description__icontains=keyword
        ) | jobs.filter(
            company__icontains=keyword
        )
    if remote:
        jobs = jobs.filter(is_remote=True)

    return render(request, "jobs/job_list.html", {"jobs": jobs})

def job_detail(request, job_id):
    return HttpResponse(f"Job detail {job_id}")

def job_create(request):
    if request.method == "POST":
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.posted_by = request.user
            job.save()
            return HttpResponse("Job created successfully!")
    else:
        form = JobForm()
    
    return render(request, "jobs/job_form.html", {"form": form})

def job_update(request, job_id):
    return HttpResponse(f"Update job {job_id}")

def job_delete(request, job_id):
    return HttpResponse(f"Delete job {job_id}")
