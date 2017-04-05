from django.db import models

# Create your models here.
class User(models.Model):
    SEX_CHOICE = (
            ('F','Female'),
            ('M', 'Male'),
    )

    name = models.CharField(max_length=30)
    age = models.IntegerField()
    sex = models.CharField(max_length=1,choices=SEX_CHOICE)

class Workout(models.Model):
    date = models.DateField(null=True)
    user = User.pk