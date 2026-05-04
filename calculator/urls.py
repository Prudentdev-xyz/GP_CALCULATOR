from django.urls import path
from . import views

urlpatterns = [
    path('setup/',           views.setup_semester, name='add_semester'),
    path('courses/',         views.add_courses,    name='add_courses'),
    path('confirm/',         views.confirm,         name='confirm'),
    path('calculate/',       views.calculate,       name='calculate'),
    path('<int:pk>/result/', views.result,          name='result'),
    path('<int:pk>/pdf/',    views.download_pdf,    name='download_pdf'),
]