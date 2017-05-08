import datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.utils.safestring import mark_safe
from .calendar_functions import WorkoutCalendar
from .models import Workout
from django.http import HttpResponse, HttpResponseRedirect
import json
from django.shortcuts import render


@login_required
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
    context = {'page': request.resolver_match.url_name,
               'user': request.user,
               'calendar': mark_safe(cal)}
    return render('calendar_template.html', context)


def display_form(request):
    print("Display form!")
    date_str = request.GET.get('date')
    print(date_str)

    if date_str != '':
        date_arr = date_str.split('-')
        workout = Workout.objects.filter(date__year=date_arr[0], date__month=date_arr[1],
                                         date__day=date_arr[2])
        to_send = ''
        for e in workout:
            print(e.id)
            to_send = {'date': str(e.date),
                       'distance': e.distance,
                       'runner': e.user.name,
                       'comment': e.comment,
                       'done': e.done,
                       'id' : e.id
                       }
        return HttpResponse(json.dumps(to_send))

    else:
        return HttpResponse()


def add_workout(request):
    if request.POST:
        print("Add workout! Data got from the form: " )
        params = request.POST
        date = datetime.datetime.strptime(request.POST.get('date'), "%Y-%m-%d").date()
        user = request.user
        print(date)
        new_workout = Workout(date=date, distance=int(params.get('distance')), comment=params.get('comment'),
                              user=user, done=False)
        new_workout.save()
    return HttpResponse(status=200)


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
