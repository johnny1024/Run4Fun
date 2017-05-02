from django.contrib import admin

# Register your models here.
from .models import Workout
from .models import Runner

admin.site.register(Workout)
admin.site.register(Runner)
