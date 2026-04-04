from django.shortcuts import render, redirect
from .models import Job, Application
from .services import create_job, apply_to_job
from accounts.decorators import admin_required, login_required


@login_required
def job_list(request):
    jobs = Job.objects()

    user_id = request.session.get('user_id')

    applied_jobs = []

    if request.session.get('role') == "candidate":
        applications = Application.objects(user_id=user_id)
        applied_jobs = [str(app.job_id) for app in applications]

    return render(request, 'jobs.html', {
        'jobs': jobs,
        'applied_jobs': applied_jobs,
        'role': request.session.get('role')
    })


@admin_required
def add_job(request):
    if request.method == "POST":
        create_job(request.POST, request.session['user_id'], request.FILES)
        return redirect('/jobs/')

    return render(request, "add_job.html")


from django.shortcuts import redirect

def apply_job(request, job_id):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('/login/?next=/jobs/apply/' + str(job_id))

    apply_to_job(job_id, user_id)
    return redirect('/candidate-dashboard/')

def company_jobs(request, company_name):
    jobs = Job.objects(company=company_name)

    return render(request, "company_jobs.html", {
        "jobs": jobs,
        "company": company_name
    })

from .services import save_job

@login_required
def save_job_view(request, job_id):
    save_job(request.session['user_id'], str(job_id))
    return redirect('/')


@admin_required
def edit_job(request, job_id):
    job = Job.objects(id=job_id).first()

    if request.method == "POST":
        create_job(request.POST, request.session['user_id'], request.FILES, job)
        return redirect('/jobs/')

    return render(request, "add_job.html", {"job": job})

@admin_required
def delete_job(request, job_id):
    job = Job.objects(id=job_id).first()

    if job:
        if job.logo:
            job.logo.delete()

        job.delete()

    return redirect('/jobs/')

from django.http import HttpResponse

def job_logo(request, job_id):
    job = Job.objects(id=job_id).first()

    if job and job.logo:
        return HttpResponse(job.logo.read(), content_type="image/png")

    return HttpResponse("No image")