# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-09-18 02:48
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('discussions', '0004_mouseclicks'),
    ]

    operations = [
        migrations.DeleteModel(
            name='MouseClicks',
        ),
    ]
