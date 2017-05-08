from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


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
    age = models.IntegerField(null=True)
    sex = models.CharField(max_length=1, choices=SEX_CHOICE, null=True)
    weight = models.FloatField(null=True)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
