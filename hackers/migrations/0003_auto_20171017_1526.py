# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-10-17 17:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hackers', '0002_auto_20171017_1432'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='cv',
            field=models.CharField(max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='application',
            name='cv_type',
            field=models.CharField(choices=[('LI', 'LinkedIn'), ('GH', 'GitHub'), ('WS', 'Website'), ('OT', 'Outro')], max_length=3, null=True),
        ),
    ]
