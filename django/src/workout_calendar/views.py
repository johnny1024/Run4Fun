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
from dateutil.relativedelta import relativedelta


@login_required
@user_passes_test(profile_data_check, '/profile/')
def calendar(request, year=None, month=None):
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
                print(obj.date)
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
        path = request.path.split('/')
        if len(path) > 3:
            year = path[-2]
            month = path[-1]
        now = datetime.datetime.now()
        if month is None:
            month = now.month
        if year is None:
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
    """
    Returns first (ordered by date) workout having given user and date

    `user`: users associated with the workout
    `date`: date associated with the workout
    """
    print('Get first workout')
    return Workout.objects.filter(user=user, date=date)[0]


def get_all_user_workouts(year, month, day, user):
    """
    Returns a list of all workouts having given user, year, month and day

    `year`: Year the user wants to display
    `month`: Month the user wants to display
    `day`: Day the user wants to display
    """
    print('Get all user workouts')
    return Workout.objects.filter(date__year=year, date__month=month,
                                  date__day=day, user=user)


def get_workouts_for_calendar(year, month, user):
    """
    Returns a list of all workouts having given user, year and month. Ordered by workout database ID.

    `year`: Year the user wants to display
    `month`: Month the user wants to display
    """
    return Workout.objects.order_by('id').filter(
        date__year=year, date__month=month, user=user
    )


def change_month(request):
    date_str = request.GET.get('date')
    direction = request.GET.get('type')
    date = datetime.datetime.strptime(date_str, '%Y-%m-%d')
    if direction == 'next':
        changed_date = date + relativedelta(months=1)
    else:
        changed_date = date - relativedelta(months=1)

    to_send = {'month': changed_date.month,
               'year': changed_date.year
               }
    return HttpResponse(json.dumps(to_send))


def get_weight(request):
    print('xd')
    user = request.user
    print(user.profile.weight)
    to_send = {'weight': user.profile.weight}
    return HttpResponse(json.dumps(to_send))
