# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-06-27 14:18
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('session', '0002_auto_20170327_1659'),
        ('subject', '0002_auto_20170327_1659'),
        ('timetable', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Wishlist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField(null=True)),
                ('semester', models.SmallIntegerField(null=True)),
                ('lectures', models.ManyToManyField(to='subject.Lecture')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wishlist_set', to='session.UserProfile')),
            ],
        ),
    ]
