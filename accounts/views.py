from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import UserProfile


def signup_view(request):
    if request.method == 'POST':
        full_name  = request.POST.get('full_name')
        email      = request.POST.get('email')
        matric     = request.POST.get('matric_number')
        department = request.POST.get('department')
        programme  = request.POST.get('programme')
        level      = request.POST.get('level')
        password1  = request.POST.get('password1')
        password2  = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, 'Passwords do not match!')
            return redirect('signup')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered!')
            return redirect('signup')

        name_parts = full_name.strip().split(' ')
        first_name = name_parts[0]
        last_name  = ' '.join(name_parts[1:]) if len(name_parts) > 1 else ''

        user = User.objects.create_user(
            username=email,
            email=email,
            password=password1,
            first_name=first_name,
            last_name=last_name,
        )

        UserProfile.objects.create(
            user=user,
            matric_number=matric,
            department=department,
            programme=programme,
            level=level,
        )

        messages.success(request, 'Account created! Please login.')
        return redirect('login')

    return render(request, 'signup.html')


def login_view(request):
    if request.method == 'POST':
        email    = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid email or password!')
            return redirect('login')

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('landing')


@login_required(login_url='/auth/login/')
def dashboard(request):
    try:
        profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        profile = None

    from calculator.models import Semester

    semesters = Semester.objects.filter(user=request.user).order_by('created_at')

    # CGPA calculation
    total_units        = 0
    total_grade_points = 0
    cgpa               = None
    overall_class      = None

    for sem in semesters:
        total_units        += sem.total_units
        total_grade_points += float(sem.total_grade_points)

    if total_units > 0:
        cgpa = round(total_grade_points / total_units, 2)

        if cgpa >= 4.50:
            overall_class = 'First Class'
        elif cgpa >= 3.50:
            overall_class = 'Second Class Upper'
        elif cgpa >= 2.40:
            overall_class = 'Second Class Lower'
        elif cgpa >= 1.50:
            overall_class = 'Third Class'
        else:
            overall_class = 'Pass'

    return render(request, 'dashboard.html', {
        'profile':   profile,
        'semesters': semesters,
        'cgpa':      cgpa,
        'overall_class': overall_class,
    })