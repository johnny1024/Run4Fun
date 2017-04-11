from django.contrib import admin

# Register your models here.
from .models import User, Workout

admin.site.register(User)
admin.site.register(Workout)