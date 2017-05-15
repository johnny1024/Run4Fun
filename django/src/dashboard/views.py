from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render_to_response


# Create your views here.
from django.urls import reverse

from accounts.views import profile_data_check


@login_required
@user_passes_test(profile_data_check, '/profile/')
def index(request):
    context = {'page': request.resolver_match.url_name,
               'user': request.user}
    return render_to_response('dashboard.html', context)
