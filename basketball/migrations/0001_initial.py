# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='League',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=50)),
                ('is_active', models.BooleanField(default=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('signup_allowed', models.BooleanField(default=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LeagueMembership',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('league', models.ForeignKey(to='basketball.League')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('position', models.CharField(default=b'G', max_length=1, choices=[(b'G', b'Guard'), (b'F', b'Forward'), (b'C', b'Center')])),
                ('name', models.CharField(max_length=50)),
                ('age', models.PositiveSmallIntegerField(validators=[django.core.validators.MaxValueValidator(100)])),
                ('about', models.TextField(max_length=250, blank=True)),
                ('leagues', models.ManyToManyField(to='basketball.League', through='basketball.LeagueMembership')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('league', models.ForeignKey(to='basketball.League')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='leaguemembership',
            name='player',
            field=models.ForeignKey(to='basketball.Player'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='leaguemembership',
            name='team',
            field=models.ForeignKey(blank=True, to='basketball.Team', null=True),
            preserve_default=True,
        ),
    ]
