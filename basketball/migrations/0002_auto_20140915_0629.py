# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('basketball', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='league',
            name='max_number_teams',
            field=models.PositiveSmallIntegerField(default=8, validators=[django.core.validators.MinValueValidator(2)]),
        ),
        migrations.AlterField(
            model_name='league',
            name='name',
            field=models.CharField(max_length=50),
        ),
    ]
