from django.shortcuts import render_to_response


# Create your views here.
def index(request):
    context = {'page': request.path.replace('/', ''),
               'logged': request.session.test_cookie_worked()}
    return render_to_response('dashboard_main.html', context)
