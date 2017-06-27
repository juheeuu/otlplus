# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-06-27 14:42
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('timetable', '0002_wishlist'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wishlist',
            name='semester',
        ),
        migrations.RemoveField(
            model_name='wishlist',
            name='year',
        ),
        migrations.AlterField(
            model_name='wishlist',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='wishlist_set', to='session.UserProfile'),
        ),
    ]