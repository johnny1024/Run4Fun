# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-24 14:59
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20170524_1455'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='age',
            field=models.PositiveIntegerField(error_messages={'invalid': 'Enter a valid value', 'required': 'This field is required'}, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='weight',
            field=models.FloatField(error_messages={'invalid': 'Enter a valid value', 'required': 'This field is required'}, null=True, validators=[django.core.validators.MinValueValidator(10.0)]),
        ),
    ]