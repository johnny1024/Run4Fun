from .models import Workout
from .calendar_functions import WorkoutCalendar
from django.utils.safestring import mark_safe
import datetime
from django.http import HttpResponse
import json
from django.shortcuts import render


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
    return render(request, 'calendar_template.html', {'calendar': mark_safe(cal), })


def display_form(request):
    print("Display form!")
    date_str = request.GET.get('date')
    if date_str != '':
        date_arr = date_str.split('-')
        workout = Workout.objects.filter(date__year=date_arr[0], date__month=date_arr[1],
                                         date__day=date_arr[2])
        to_send = ''
        for e in workout:
            print(e.distance)
            to_send = {'date': str(e.date),
                       'distance': e.distance,
                       'runner': e.user.name,
                       'comment': e.comment,
                       'done': e.done
                       }
        return HttpResponse(json.dumps(to_send))

    else:
        return HttpResponse()


def add_workout(request):
    if request.POST:
        print("Add workout! Data got from the form: " )
        print(request.body)
        print(request.POST.get('runner'))
    return HttpResponse()


def update_workout(request):
    if request.POST:
        print("Update workout! Data got from the form: " )
        print(request.body)
        print(request.POST.get('runner'))
    return HttpResponse()


def delete_workout(request):
    if request.POST:
        print("Delete workout! Data got from the form: " )
        print(request.body)
        print(request.POST.get('runner'))
    return HttpResponse()
