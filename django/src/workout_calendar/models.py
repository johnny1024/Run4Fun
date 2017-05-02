from django.db import models


# Create your models here.
class Runner(models.Model):
    """
    Class that represents single user in application.
    It contains basic information about user.

    `name`: User's chosen name.
    `age`: User's age.
    `sex`: User's sex.
    """
    SEX_CHOICE = (
        ('F', 'Female'),
        ('M', 'Male'),
    )

    name = models.CharField(max_length=30)
    age = models.IntegerField()
    sex = models.CharField(max_length=1, choices=SEX_CHOICE)


class Workout(models.Model):
    """
    Class that represents single training.
    When User wants to add training to calendar, Workout object is created.
    It contains important information about training.

    `date`: date of training.
    `user`: User's name.
    `title`: short description of planned training.
    """
    date = models.DateField(null=True)
    distance = models.IntegerField(null=True)
    comment = models.TextField(blank=True)
    user = models.ForeignKey(Runner, on_delete=models.CASCADE, null=True)
    done = models.BooleanField(default=False)