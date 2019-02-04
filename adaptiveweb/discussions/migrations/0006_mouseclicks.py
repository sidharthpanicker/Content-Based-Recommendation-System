# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-09-18 02:50
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('discussions', '0005_delete_mouseclicks'),
    ]

    operations = [
        migrations.CreateModel(
            name='MouseClicks',
            fields=[
                ('auto_increment_id', models.AutoField(primary_key=True, serialize=False)),
                ('operation_type', models.TextField()),
                ('post_id', models.TextField()),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('approved_comment', models.BooleanField(default=False)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
