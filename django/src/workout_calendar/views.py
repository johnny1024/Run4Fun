from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.safestring import mark_safe
from workout_calendar.form import WorkoutForm
from accounts.views import profile_data_check
from .calendar_functions import WorkoutCalendar
from .models import Workout
from django.http import HttpResponse
from django.shortcuts import render, redirect
import json
import datetime


@login_required
@user_passes_test(profile_data_check, '/profile/')
def calendar(request, year, month):
    """
    Given a year and a month, executes database queries, gets Workout list and allows the user to
    create new Workout, delete or update an existing one.

    `request`: GET or POST request
    `year`: Year the user wants to display
    `month`: Month the user wants to display

    Redirects to calendar, updates, deletes or creates records in database.
    """
    if request.method == 'POST':
        form = WorkoutForm(request.POST)
        if 'create' in request.POST:
            if form.is_valid():
                obj = form.save(commit=False)
                print(obj.id)
                obj.user = request.user
                obj.save()
                return redirect('calendar')
        else:
            if form.is_valid():
                obj = form.save(commit=False)
                workout = get_first_workout(request.user, obj.date)
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
        my_workouts = get_workouts_for_calendar(year, month, request.user)
        form = WorkoutForm()
        cal = WorkoutCalendar(my_workouts).formatmonth(year, month)
        context = {'page': request.resolver_match.url_name,
                   'user': request.user,
                   'calendar': mark_safe(cal),
                   'form': form}
        return render(request, 'calendar.html', context)


def display_form(request):
    """
    Displays form. Gets the workouts from database and sends the data back to javascript.

    `request`: GET request with date of the clicked calendar day.

    Method returns HttpResponse with status 200 or 404
    """
    date_str = request.GET.get('date')
    print(date_str)
    if date_str:
        date_arr = date_str.split('-')
        workout = get_all_user_workouts(year=date_arr[0], month=date_arr[1],
                                        day=date_arr[2], user=request.user)
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


def get_first_workout(user, date):
    print('Get first workout')
    return Workout.objects.filter(user=user, date=date)[0]


def get_all_user_workouts(year, month, day, user):
    print('Get all user workouts')
    return Workout.objects.filter(date__year=year, date__month=month,
                                  date__day=day, user=user)


def get_workouts_for_calendar(year, month, user):
    return Workout.objects.order_by('id').filter(
        date__year=year, date__month=month, user=user
    )
