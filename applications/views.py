from django.shortcuts import render
from django.http import HttpResponse
from .models import Application
from django.views import View
from .forms import ApplicationForm

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .forms import ApplicationForm
from jobs.models import Job

@login_required
def application_create(request, job_id):
    job = get_object_or_404(Job, pk=job_id)   # fetch the job safely
    
    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.user = request.user
            application.save()
            return redirect('job_detail', job_id=job.id)  # redirect instead of HttpResponse
    else:
        form = ApplicationForm()
    
    return render(request, 'applications/application_form.html', {'form': form, 'job': job})
