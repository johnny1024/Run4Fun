from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MinValueValidator

my_default_errors = {
    'required': 'This field is required',
    'invalid': 'Enter a valid value'
}


class Profile(models.Model):
    """
    Extends the user model by storing not authentication-related data.

    `user`: User's ID.
    `age`: User's age.
    `sex`: User's sex.
    `weight`: User's weight
    """

    SEX_CHOICE = (
        ('F', 'Female'),
        ('M', 'Male'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.PositiveIntegerField(null=True, error_messages=my_default_errors)
    sex = models.CharField(max_length=1, choices=SEX_CHOICE, null=False, default=SEX_CHOICE[1][0])
    weight = models.FloatField(null=True, validators=[MinValueValidator(10.0)], error_messages=my_default_errors)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Triggered when user is created. Creates user in database.
    """
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    Triggered when user profile is updated. Saves updated profile in database.
    """
    instance.profile.save()
