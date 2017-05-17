import datetime
from django.contrib.auth.decorators import login_required
from django.utils.safestring import mark_safe
from workout_calendar.form import WorkoutForm
from .calendar_functions import WorkoutCalendar
from .models import Workout
from django.http import HttpResponse
import json
from django.shortcuts import render, redirect


@login_required
def calendar(request, year, month):
    """
    If the request is a POST request, validates the form and creates, updates or deletes a chosen workout.

    Otherwise, displays the main calendar.
    `param`: request: GET or POST request made by a logged user.
    `param year`: String representing a year we want to display.
    `param month`: String representing a month we want to display

    Method returns HttpResponse redirecting to calendar.html
    """
    if request.method == 'POST':
        form = WorkoutForm(request.POST)
        print(form)
        if 'create' in request.POST:
            if form.is_valid():
                obj = form.save(commit=False)
                print(obj.id)
                obj.user = request.user
                obj.save()
                print("saved")
                return redirect('calendar')
        else:
            if form.is_valid():
                obj = form.save(commit=False)
                workout = Workout.objects.filter(user=request.user, date=obj.date)[0]
                if 'update' in request.POST:
                    f = WorkoutForm(request.POST, instance=workout)
                    f.save()
                elif 'delete' in request.POST:
                    workout.delete()
        return redirect('calendar')
    else:
        now = datetime.datetime.now()
        if len(month) == 0:
            month = now.month
        if len(year) == 0:
            year = now.year
        month = int(month)
        year = int(year)
        my_workouts = Workout.objects.order_by('id').filter(
            date__year=year, date__month=month, user=request.user
        )
        form = WorkoutForm()
        cal = WorkoutCalendar(my_workouts).formatmonth(year, month)
        context = {'page': request.resolver_match.url_name,
                   'user': request.user,
                   'calendar': mark_safe(cal),
                   'form': form}
        return render(request, 'calendar.html', context)


def display_form(request):
    """
    Gets all of the user workouts at a chosen date and passes the result to the javascript function.

    `param:` request: GET request with a date.
    """
    date_str = request.GET.get('date')
    print(date_str)
    if date_str:
        date_arr = date_str.split('-')
        workout = Workout.objects.filter(date__year=date_arr[0], date__month=date_arr[1],
                                         date__day=date_arr[2], user=request.user)
        to_send = ''
        for e in workout:
            print("title " + e.title)
            to_send = {'date': str(e.date),
                       'distance': e.distance,
                       'title': e.title,
                       'runner': request.user.username,
                       'comment': e.comment,
                       'done': e.done,
                       'id': e.id
                       }
        return HttpResponse(json.dumps(to_send))
    else:
        return HttpResponse(status=404)
