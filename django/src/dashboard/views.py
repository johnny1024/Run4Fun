from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response


# Create your views here.
@login_required
def index(request):
    context = {'page': request.resolver_match.url_name,
               'user': request.user}
    return render_to_response('dashboard.html', context)
