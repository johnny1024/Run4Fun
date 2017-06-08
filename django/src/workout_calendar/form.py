from django import forms

from workout_calendar.models import Workout


class WorkoutForm(forms.ModelForm):
    """
    Form that allows the user to modify and save Workouts.
    """
    calories = forms.IntegerField()
    time = forms.IntegerField()

    class Meta:
        model = Workout
        fields = ('id', 'date', 'title', 'distance', 'calories',
                  'time', 'comment', 'done')
        # date= forms.CharField(disabled=True)
