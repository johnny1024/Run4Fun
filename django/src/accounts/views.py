from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render, render_to_response
from django.urls import reverse


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


@login_required
def profile(request):
    context = {'page': request.resolver_match.url_name,
               'user': request.user}
    return render_to_response('profile.html', context)


@login_required
def index(request):
    return HttpResponseRedirect(reverse('profile'))
