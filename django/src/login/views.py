from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response


# Create your views here.
def index(request):
    request.session.set_test_cookie()
    # context = {'page': request.path.replace('/', ''),
    #            'logged': request.session.test_cookie_worked()}
    return HttpResponseRedirect('/dashboard')


def logout(request):
    request.session.delete_test_cookie()
    context = {'page': request.path.replace('/', ''),
               'logged': request.session.test_cookie_worked()}
    return render_to_response('dashboard_main.html', context)
