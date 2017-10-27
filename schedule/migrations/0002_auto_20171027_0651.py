# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-10-27 08:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hackers', '0006_hacker_second_chance'),
        ('schedule', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attendee',
            name='hacker',
        ),
        migrations.AddField(
            model_name='attendee',
            name='hacker',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='events_attended', to='hackers.Hacker'),
        ),
    ]
