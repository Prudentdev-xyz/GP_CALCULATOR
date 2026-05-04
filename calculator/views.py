from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Semester, Course
from .utils import grade_point, calculate_gp
from accounts.models import UserProfile
from django.http import HttpResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa
import io
from accounts.models import UserProfile

@login_required(login_url='/auth/login/')
def setup_semester(request):
    # Block if semester already exists
    if Semester.objects.filter(user=request.user).exists():
        messages.error(request, 'You have already entered your semester!')
        return redirect('dashboard')

    if request.method == 'POST':
        semester_name = request.POST.get('semester_name')
        academic_year = request.POST.get('academic_year')
        num_courses   = request.POST.get('num_courses')

        if not semester_name or not academic_year or not num_courses:
            messages.error(request, 'Please fill all fields!')
            return redirect('add_semester')

        request.session['semester_name'] = semester_name
        request.session['academic_year'] = academic_year
        request.session['num_courses']   = int(num_courses)

        return redirect('add_courses')

    return render(request, 'calculator/setup.html')

@login_required(login_url='/auth/login/')
def add_courses(request):
    num_courses   = request.session.get('num_courses', 1)
    semester_name = request.session.get('semester_name', '')
    academic_year = request.session.get('academic_year', '')

    if request.method == 'POST':
        courses = []
        errors  = []

        for i in range(num_courses):
            code  = request.POST.get(f'course_code_{i}', '').strip()
            unit  = request.POST.get(f'credit_unit_{i}', '')
            score = request.POST.get(f'score_{i}', '')

            if not code or not unit or not score:
                errors.append(f'Row {i+1}: All fields are required.')
                continue

            try:
                unit  = int(unit)
                score = int(score)
            except ValueError:
                errors.append(f'Row {i+1}: Unit and Score must be numbers.')
                continue

            if not (1 <= unit <= 6):
                errors.append(f'Row {i+1}: Credit unit must be between 1 and 6.')
            if not (0 <= score <= 100):
                errors.append(f'Row {i+1}: Score must be between 0 and 100.')

            courses.append({
                'course_code': code,
                'credit_unit': unit,
                'score':       score,
            })

        if errors:
            for err in errors:
                messages.error(request, err)
            return render(request, 'calculator/courses.html', {
                'num_courses':   num_courses,
                'num_range': range(num_courses),
                'semester_name': semester_name,
                'academic_year': academic_year,
            })

        # Save to session for confirm page
        request.session['courses'] = courses
        return redirect('confirm')

    return render(request, 'calculator/courses.html', {
    'num_courses':   num_courses,
    'num_range':     range(num_courses),
    'semester_name': semester_name,
    'academic_year': academic_year,
     })


@login_required(login_url='/auth/login/')
def confirm(request):
    courses       = request.session.get('courses', [])
    semester_name = request.session.get('semester_name', '')
    academic_year = request.session.get('academic_year', '')

    if not courses:
        return redirect('add_semester')

    # Preview calculation
    courses_copy = [c.copy() for c in courses]
    gp, total_units, total_gp, degree_class = calculate_gp(courses_copy)

    return render(request, 'calculator/confirm.html', {
        'courses':       courses_copy,
        'semester_name': semester_name,
        'academic_year': academic_year,
        'gp':            gp,
        'total_units':   total_units,
        'total_gp':      total_gp,
        'degree_class':  degree_class,
    })


@login_required(login_url='/auth/login/')
def calculate(request):
    if request.method != 'POST':
        return redirect('add_semester')

    courses       = request.session.get('courses', [])
    semester_name = request.session.get('semester_name', '')
    academic_year = request.session.get('academic_year', '')

    if not courses:
        return redirect('add_semester')

    # Run GP engine
    courses_copy = [c.copy() for c in courses]
    gp, total_units, total_gp, degree_class = calculate_gp(courses_copy)

    # Save Semester to DB
    semester = Semester.objects.create(
        user               = request.user,
        semester_name      = semester_name,
        academic_year      = academic_year,
        total_units        = total_units,
        total_grade_points = total_gp,
        gp                 = gp,
        degree_class       = degree_class,
    )

    # Save each Course to DB
    for c in courses_copy:
        Course.objects.create(
            semester     = semester,
            course_code  = c['course_code'],
            credit_unit  = c['credit_unit'],
            score        = c['score'],
            grade_point  = c['grade_point'],
            grade_letter = c['grade_letter'],
        )

    # Clear session
    for key in ['courses', 'semester_name', 'academic_year', 'num_courses']:
        request.session.pop(key, None)

    return redirect('result', pk=semester.id)


@login_required(login_url='/auth/login/')
def result(request, pk):
    semester = get_object_or_404(Semester, id=pk, user=request.user)
    courses  = semester.courses.all()

    return render(request, 'calculator/result.html', {
        'semester': semester,
        'courses':  courses,
    })

@login_required(login_url='/auth/login/')
def download_pdf(request, pk):
    semester = get_object_or_404(Semester, id=pk, user=request.user)
    courses  = semester.courses.all()

    try:
        profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        profile = None

    html_string = render_to_string('calculator/result_pdf.html', {
        'semester': semester,
        'courses':  courses,
        'user':     request.user,
        'profile':  profile,
    })

    buffer = io.BytesIO()
    pisa.CreatePDF(html_string, dest=buffer)
    pdf = buffer.getvalue()
    buffer.close()

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="GP_Result_{semester.academic_year}.pdf"'
    return response