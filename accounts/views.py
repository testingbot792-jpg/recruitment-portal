from django.shortcuts import render, redirect
from mongoengine.errors import NotUniqueError

from jobs.models import Job, Application
from accounts.models import User
from .services import create_user, authenticate_user
from accounts.decorators import login_required, admin_required


# =========================
# 🔐 SIGNUP
# =========================
def signup(request):
    if request.method == "POST":
        try:
            create_user(
                request.POST.get('email'),
                request.POST.get('password'),
                request.POST.get('role')
            )
            return redirect('/login/')

        except ValueError as e:
            return render(request, "signup.html", {"error": str(e)})

        except NotUniqueError:
            return render(request, "signup.html", {"error": "Email already exists"})

    return render(request, 'signup.html')


# =========================
# 🔐 LOGIN
# =========================
def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate_user(email, password)

        if user:
            request.session['user_id'] = str(user.id)
            request.session['role'] = user.role

            # 🔥 handle redirect after login
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)

            if user.role == "admin":
                return redirect('/dashboard/')
            else:
                return redirect('/candidate-dashboard/')

        return render(request, 'login.html', {"error": "Invalid credentials"})

    return render(request, 'login.html')


# =========================
# 🏠 HOME (with search + login modal)
# =========================
from jobs.models import Job, Application
from accounts.models import User
from django.shortcuts import render, redirect
from .services import authenticate_user

def home(request):
    jobs = Job.objects()

    # 🔍 SEARCH
    search = request.GET.get("search", "")
    location = request.GET.get("location", "")

    if search:
        jobs = jobs.filter(title__icontains=search)

    if location:
        jobs = jobs.filter(location__icontains=location)

    # ✅ SESSION DATA
    user_id = request.session.get('user_id')
    role = request.session.get('role')

    # ✅ FIX: define applied_jobs
    applied_jobs = []
    if request.session.get('user_id'):
        apps = Application.objects(user_id=request.session['user_id'])
        applied_jobs = [str(a.job_id) for a in apps]
    
    if user_id:
        applied_jobs = [
            str(app.job_id)
            for app in Application.objects(user_id=user_id)
        ]

    # 🔐 LOGIN LOGIC
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate_user(email, password)

        if user:
            request.session['user_id'] = str(user.id)
            request.session['role'] = user.role

            if user.role == "admin":
                return redirect('/dashboard/')
            else:
                return redirect('/candidate-dashboard/')
        else:
            return render(request, 'home.html', {
                "error": "Invalid email or password",
                "jobs": jobs,
                "jobs_count": jobs.count(),
                "users_count": User.objects().count(),
                "role": role,
                "applied_jobs": applied_jobs
            })

    return render(request, 'home.html', {
        "jobs": jobs,
        "jobs_count": jobs.count(),
        "users_count": User.objects().count(),
        "role": role,
        "applied_jobs": applied_jobs
    })


# =========================
# 📊 ADMIN DASHBOARD
# =========================
@admin_required
def dashboard(request):
    jobs = Job.objects()
    users = User.objects()

    context = {
        "jobs": jobs,
        "jobs_count": jobs.count(),
        "users_count": users.count(),
        "applications_count": Application.objects().count()
    }

    return render(request, "dashboard.html", context)


# =========================
# 👤 CANDIDATE DASHBOARD
# =========================
from django.shortcuts import render, redirect
from accounts.decorators import login_required
from jobs.models import Job, Application
from accounts.models import User


@login_required
def candidate_dashboard(request):
    user_id = request.session.get('user_id')

    user = User.objects(id=user_id).first()
    applications = Application.objects(user_id=user_id)

    jobs = []
    for app in applications:
        job = Job.objects(id=app.job_id).first()
        if job:
            jobs.append({
                "id": str(job.id),
                "title": job.title,
                "company": job.company,
                "location": job.location,
                "status": app.status
            })

    return render(request, "candidate_dashboard.html", {
        "jobs": jobs,
        "user": user
    })


# =========================
# 📄 UPLOAD RESUME
# =========================
@login_required
def upload_resume(request):
    if request.method == "POST":
        user = User.objects(id=request.session['user_id']).first()

        file = request.FILES.get('resume')

        if not file:
            print("❌ No file received")
            return redirect('/candidate-dashboard/')

        # Delete old resume
        if user.resume:
            user.resume.delete()

        # Save new resume
        user.resume.put(file, content_type=file.content_type)
        user.save()

        print("✅ Resume uploaded")

    return redirect('/candidate-dashboard/')

@login_required
def delete_resume(request):
    user = User.objects(id=request.session['user_id']).first()

    if user and user.resume:
        user.resume.delete()
        user.save()

    return redirect('/candidate-dashboard/')


# =========================
# 🚪 LOGOUT
# =========================
def logout_view(request):
    request.session.flush()
    return redirect('/')


# =========================
# 🚪 Candidate list
# =========================
from accounts.decorators import admin_required
from .models import User

@admin_required
def candidate_list(request):
    candidates = User.objects(role="candidate")

    return render(request, "candidate_list.html", {
        "candidates": candidates
    })

from django.http import HttpResponse

from django.http import HttpResponse
from accounts.models import User

def view_resume(request, user_id):
    session_user_id = request.session.get('user_id')
    role = request.session.get('role')
    if not session_user_id:
        return redirect('/')
    user = User.objects(id=user_id).first()
    if not user or not user.resume:
        return HttpResponse("No resume found")
    if role != "admin" and str(user.id) != session_user_id:
        return redirect('/')
    response = HttpResponse(user.resume.read(), content_type="application/pdf")
    response['Content-Disposition'] = f'inline; filename="{user.resume.filename}"'
    return response

from accounts.decorators import login_required
from accounts.models import User

@login_required
def profile(request):
    user = User.objects(id=request.session['user_id']).first()

    if request.method == "POST":
        user.name = request.POST.get("name")
        user.phone = request.POST.get("phone")
        user.address = request.POST.get("address")

        # resume upload
        if request.FILES.get("resume"):
            if user.resume:
                user.resume.replace(request.FILES["resume"])
            else:
                user.resume.put(request.FILES["resume"], filename=request.FILES["resume"].name)

        user.save()

        return redirect('/candidate-dashboard/')

    return render(request, "profile.html", {"user": user})