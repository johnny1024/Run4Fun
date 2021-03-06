from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import transaction, connection
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render, render_to_response
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login

from accounts.form import ProfileForm


def profile_data_check(user):
    return user.profile.age is not None


def signup(request):
    """
    View for displaying a signup form. Redirects to Profile page after successful registration

    `request`: request o extract post information from

    In case of POST request this view performs user creation in the database, otherwise displays a registration form.
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('profile')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


@login_required
@transaction.atomic
def profile(request):
    """
    View for displaying user's profile.

    `request`: request for this view.

    On this view user can add and edit his account information.
    This view requires being logged.
    """
    if request.method == 'POST':
        user_form = request.user
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if profile_form.is_valid():
            profile_form.save()
            return redirect('profile')
        else:
            print("forms are not valid")
    else:
        user_form = request.user
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'profile.html', {
        'user': user_form,
        'profile_form': profile_form,
        'page': request.resolver_match.url_name
    })


@login_required
def index(request):
    """
    Redirects user to the profile page

    `request`: request for this view.

    Returns profile page if user accessed '/' and is logged
    """
    return HttpResponseRedirect(reverse('profile'))


def clear_db(request):
    """
    Removes all users and their data from database

    `request`: request for this view.

    """
    if connection.settings_dict['NAME'] == 'test_db':
        User.objects.all().delete()
    return render_to_response('home.html')
