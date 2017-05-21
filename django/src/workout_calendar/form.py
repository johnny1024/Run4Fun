from django import forms

from workout_calendar.models import Workout


class WorkoutForm(forms.ModelForm):
    class Meta:
        model = Workout
        fields = ('id', 'date', 'title', 'distance', 'comment', 'done')
    # date= forms.CharField(disabled=True)