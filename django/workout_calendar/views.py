from django.shortcuts import render
from django.http import HttpResponse
from .models import User, Workout
from django.template import loader
from django.http import Http404
from workout_calendar.calendar_functions import WorkoutCalendar
from django.shortcuts import render_to_response
from django.utils.safestring import mark_safe
import datetime


def calendar(request, year, month):
    now = datetime.datetime.now()
    if len(month) == 0:
        month = now.month
    if len(year) == 0:
        year = now.year
    month = int(month)
    year = int(year)
    my_workouts = Workout.objects.order_by('id').filter(
        date__year=year, date__month=month
    )
    cal = WorkoutCalendar(my_workouts).formatmonth(year, month)
    return render_to_response('calendar_template.html', {'calendar': mark_safe(cal), })
