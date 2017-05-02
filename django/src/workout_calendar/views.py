import datetime
from django.shortcuts import render_to_response
from django.utils.safestring import mark_safe

from .calendar_functions import WorkoutCalendar
from .models import Workout


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
    context = {'page': request.path.replace('/', ''),
               'logged': request.session.test_cookie_worked(),
               'calendar': mark_safe(cal)}
    return render_to_response('calendar_template.html', context)
