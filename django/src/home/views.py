from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response


# Create your views here.
from django.urls import reverse


def index(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('dashboard'))
    else:
        return render_to_response('home.html')
