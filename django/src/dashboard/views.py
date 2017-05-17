from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render_to_response
from workout_calendar.models import Workout
from django.utils import timezone
from datetime import timedelta

from accounts.views import profile_data_check


@login_required
@user_passes_test(profile_data_check, '/profile/')
def index(request):
    context = {'page': request.resolver_match.url_name,
               'user': request.user,
               'days': days_since_join(request.user),
               'distanceWhole': whole_ran_distance(request.user),
               'distanceWeekDone': weekly_run(request.user)[0],
               'distanceWeekPlanned': weekly_run(request.user)[1]}
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
