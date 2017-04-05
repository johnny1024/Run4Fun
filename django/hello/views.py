from django.shortcuts import render
from django.http import HttpResponse
from .models import User, Workout
from django.template import loader
from django.http import Http404
from hello.calendar_functions import WorkoutCalendar
from django.shortcuts import render_to_response
from django.utils.safestring import mark_safe


def index(request):
    latest_users_list = User.objects.order_by('-name')
    template = loader.get_template('hello/index.html')
    context = { 'latest_users_list': latest_users_list,
                }
    # return HttpResponse(template.render(context, request))
    return render(request, 'hello/index.html', context)

def display_user(request, user_id):
    # return HttpResponse("You're looking at user" + str(user_id))
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        raise Http404("User does not exist")
    return render(request, 'hello/user.html', {'user': user})


def calendar(request, year, month):

  month = int(month)
  year = int(year)
  my_workouts = Workout.objects.order_by('id').filter(
    date__year=year, date__month=month
  )
  cal = WorkoutCalendar(my_workouts).formatmonth(year, month)
  return render_to_response('hello/my_template.html', {'calendar': mark_safe(cal),})