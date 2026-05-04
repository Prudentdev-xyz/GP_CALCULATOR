from django.db import models
from django.contrib.auth.models import User


class Semester(models.Model):
    SEMESTER_CHOICES = [
        ('1st Semester', '1st Semester'),
        ('2nd Semester', '2nd Semester'),
    ]

    user             = models.ForeignKey(User, on_delete=models.CASCADE)
    semester_name    = models.CharField(max_length=50, choices=SEMESTER_CHOICES)
    academic_year    = models.CharField(max_length=20)
    total_units      = models.IntegerField(default=0)
    total_grade_points = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    gp               = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    degree_class     = models.CharField(max_length=50, blank=True)
    created_at       = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.get_full_name()} — {self.semester_name} {self.academic_year}"


class Course(models.Model):
    semester     = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name='courses')
    course_code  = models.CharField(max_length=20)
    credit_unit  = models.IntegerField()
    score        = models.IntegerField()
    grade_point  = models.IntegerField(default=0)
    grade_letter = models.CharField(max_length=2, default='F')

    def __str__(self):
        return f"{self.course_code} — {self.grade_letter}"