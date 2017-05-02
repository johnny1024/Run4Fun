from django.shortcuts import render_to_response


def index(request):
    context = {'page': request.path.replace('/', ''),
               'logged': request.session.test_cookie_worked()}
    return render_to_response('profile_main.html', context)
