from django import forms

from accounts.models import Profile


class ProfileForm(forms.ModelForm):
    """
    A form used in Profile page for editing and validation purposes
    """
    class Meta:
        model = Profile
        fields = ('age', 'sex', 'weight')
