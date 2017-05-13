from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render, render_to_response
from django.urls import reverse

from accounts.form import ProfileForm


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


# @login_required
# @transaction.atomic
# def profile(request):
#     context = {'page': request.resolver_match.url_name,
#                'user': request.user}
#     return render_to_response('profile.html', context)


@login_required
@transaction.atomic
def profile(request):
    if request.method == 'POST':
        user_form = request.user
        # user_form = UserCreationForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if profile_form.is_valid(): #and user_form.is_valid():
            print("forms are ""valid")
            user_form.save()
            profile_form.save()
            print("profile saved?")
            # messages.success(request, _('Your profile was successfully updated!'))
            return redirect('profile')
        else:
            print("forms are not valid")
            # messages.error(request, _('Please correct the error below.'))
    else:
        user_form = request.user
        # user_form = UserCreationForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'profile.html', {
        'user': user_form,
        'profile_form': profile_form
    })


@login_required
def index(request):
    return HttpResponseRedirect(reverse('profile'))
