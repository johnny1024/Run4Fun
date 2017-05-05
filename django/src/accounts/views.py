from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response


# Create your views here.
# def index(request):
#     request.session.set_test_cookie()
#     # context = {'page': request.path.replace('/', ''),
#     #            'logged': request.session.test_cookie_worked()}
#     return HttpResponseRedirect('/dashboard')

def index(request):
    print("test")

    return render_to_response('login.html')


def auth_and_redirect(request):
    context = {'page': request.path.replace('/', ''),
               'logged': request.session.test_cookie_worked()}
    if request.session.test_cookie_worked:
        return render_to_response('dashboard_main.html', context)
    else:
        return render_to_response('login_main.html', context)


def register(request):
    print("test")

    return HttpResponseRedirect('/dashboard')


def logout(request):
    request.session.delete_test_cookie()
    context = {'page': request.path.replace('/', ''),
               'logged': request.session.test_cookie_worked()}
    return render_to_response('dashboard_main.html', context)
