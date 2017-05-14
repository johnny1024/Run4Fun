from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render, render_to_response
from django.urls import reverse
from accounts.form import ProfileForm
from run4fun.settings import AVATARS_DIR, DEFAULT_AVATAR_DIR


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
@transaction.atomic
def profile(request):
    if request.method == 'POST':
        user_form = request.user
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if profile_form.is_valid():
            print("forms are ""valid")

            # TODO not working
            avatar = profile_form.cleaned_data['avatar']
            profile_form.avatar = avatar

            user_form.save()
            profile_form.save()
            print("profile saved?")
            return redirect('profile')
        else:
            print("forms are not valid")
    else:
        user_form = request.user
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'profile.html', {
        'user': user_form,
        'profile_form': profile_form,
        'page': request.resolver_match.url_name,
        'default_avatar_dir': DEFAULT_AVATAR_DIR,
        'avatars_dir': AVATARS_DIR
    })


@login_required
def index(request):
    return HttpResponseRedirect(reverse('profile'))
