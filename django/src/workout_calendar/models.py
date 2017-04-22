from django.db import models

# Create your models here.
class User(models.Model):
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
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=30, null=True)