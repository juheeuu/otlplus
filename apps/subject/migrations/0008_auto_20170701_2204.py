# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-07-01 13:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subject', '0007_remove_classtime_roomnum_en'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classtime',
            name='roomNum',
            field=models.CharField(max_length=20, null=True),
        ),
    ]