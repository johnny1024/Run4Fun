from django.contrib.auth.models import User
from django.db import models
# from django.db.models.signals import post_save
# from django.dispatch import receiver


class Workout(models.Model):
    """
    Represents a single training.
    When User wants to add a training to the calendar, the Workout object is created.
    It contains important information about training.

    `user`: User's name.
    `date`: date of training.
    `title`: short description of planned training.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    date = models.DateField(null=True)
    title = models.CharField(max_length=30, null=True)


# @receiver(post_save, sender=User)
# def save_user_workout(sender, instance, **kwargs):
#     if instance.workout:
#         instance.workout.save()
