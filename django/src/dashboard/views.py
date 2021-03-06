from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render_to_response
from workout_calendar.models import Workout
from django.utils import timezone
from datetime import timedelta

from accounts.views import profile_data_check

import requests


@login_required
@user_passes_test(profile_data_check, '/profile/')
def index(request):
    """
    Renders dashboard page if users is logged and has profile information filled.

    `request`: request for this view.
    """
    context = {'page': request.resolver_match.url_name,
               'user': request.user,
               'days': days_since_join(request.user),
               'distanceWhole': whole_ran_distance(request.user),
               'distanceWeekDone': weekly_run(request.user)[0],
               'distanceWeekPlanned': weekly_run(request.user)[1],
               'doneTrainings': done_trainings(request.user)[0],
               'allTrainings': done_trainings(request.user)[1],
               'temperature': get_temperature()}
    return render_to_response('dashboard.html', context)


def days_since_join(user):
    """
    Method calculates days since creation of user account.

    `user`: currently logged user

    Method returns number of days since creation of user account.
    """
    return (timezone.now() - user.date_joined).days


def whole_ran_distance(user):
    """
    Method calculates distance ran by user (all completed trainings in database).

    `user`: currently logged user

    Method returns global completed distance.
    """
    distance = 0
    workouts = Workout.objects.filter(user=user, done=True)
    for w in workouts:
        distance += w.distance
    return distance


def weekly_run(user):
    """
    Method calculates planned trainings in current week (from monday to sunday), and checks level of completion.

    `user`: currently logged user

    Method returns planned and completed distance in current week.
    """
    number_of_today = timezone.now().weekday()
    start = timezone.now() - timedelta(days=number_of_today)
    end = timezone.now() + timedelta(days=6 - number_of_today)
    workouts = Workout.objects.filter(user=user)
    planned = 0
    done = 0
    for workout in workouts:
        if start.date() <= workout.date <= end.date():
            planned += workout.distance
            if workout.done:
                done += workout.distance
    return done, planned


def done_trainings(user):
    """
    Method calculates number of all planned and all done trainings

    `user`: currently logged user

    Method return number of planned and done trainings
    """
    count_all = 0
    count_done = 0
    workouts = Workout.objects.filter(user=user)
    for workout in workouts:
        if workout.date <= timezone.now().date():
            count_all += 1
            if workout.done:
                count_done += 1
    return count_done, count_all


def get_temperature():
    """
    Method that gets the current temperature in Poznan from Open Weather API.

    Method returns current temperature in Celsius degrees.
    """
    API_KEY = '9a0e5de6bf9fbbf49481d6df5e81c320'
    POZNAN_CODE = '3088171'
    r = requests.get(
        'http://api.openweathermap.org/data/2.5/forecast?id=%s&APPID=%s&units=metric' % (POZNAN_CODE, API_KEY))
    main_json = (r.json()['list'])
    temperature = main_json[0]["main"]["temp"]
    return temperature
