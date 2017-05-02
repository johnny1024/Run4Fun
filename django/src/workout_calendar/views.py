from .models import Workout
from .calendar_functions import WorkoutCalendar
from django.shortcuts import render_to_response
from django.utils.safestring import mark_safe
import datetime
from django.utils.dateparse import parse_date
from django.http import HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt


def calendar(request, year, month):
    print("calendar!!")
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

def display_form(request):
    date_str = request.GET.get('date')
    if date_str != '':
        date_arr = date_str.split('-')
        print(date_arr[0])
        workout = Workout.objects.filter(date__year=date_arr[0], date__month=date_arr[1],
                                           date__day=date_arr[2])
        to_send = ''
        for e in workout:
            print(e.distance)
            to_send = {'date': str(e.date),
                       'distance' : e.distance,
                       'runner' : e.user.name,
                       'comment' : e.comment,
                       'done' : e.done}
        print("xd")
        return HttpResponse(json.dumps(to_send))

    else:
        return HttpResponse()


def add_workout(request):
    form_data = request.GET.get('data')
    print("Add workout! Data gotten from the form: " + str(form_data))


def update_workout(request):
    form_data = request.GET.get('data')
    print("Update workout! Data gotten from the form: " + str(form_data))


def delete_workout(request):
    form_data = request.GET.get('data')
    print("Delete workout! Data gotten from the form: " + str(form_data))