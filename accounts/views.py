from django.shortcuts import render, redirect
from .services import create_user, authenticate_user

def signup(request):
    if request.method == "POST":
        create_user(
            request.POST['email'],
            request.POST['password'],
            request.POST['role']
        )
        return redirect('/login/')
    return render(request, 'signup.html')


def login_view(request):
    if request.method == "POST":
        user = authenticate_user(
            request.POST['email'],
            request.POST['password']
        )

        if user:
            request.session['user_id'] = str(user.id)
            request.session['role'] = user.role
            return redirect('/dashboard/')
    return render(request, 'login.html')

def dashboard(request):   # 👈 ADD THIS
    return render(request, 'dashboard.html')