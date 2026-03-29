from django.shortcuts import render, redirect
from .models import Job
from .services import create_job, apply_to_job
from accounts.decorators import admin_required, login_required

@login_required
def job_list(request):
    jobs = Job.objects()
    return render(request, 'jobs.html', {'jobs': jobs})


@admin_required
def add_job(request):
    if request.method == "POST":
        create_job(request.POST, request.session['user_id'])
        return redirect('/jobs/')
    return redirect('/dashboard/')


@login_required
def apply_job(request, job_id):
    apply_to_job(job_id, request.session['user_id'])
    return redirect('/jobs/')