# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-07-01 12:51
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('subject', '0006_auto_20170701_2111'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='classtime',
            name='roomNum_en',
        ),
    ]
