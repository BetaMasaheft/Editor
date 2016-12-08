# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-10-14 15:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EditField',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('field', models.CharField(max_length=100)),
                ('field_type', models.CharField(max_length=100)),
                ('config_string', models.CharField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='EditForm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_type', models.CharField(max_length=100)),
                ('form_fields', models.ManyToManyField(to='edit_forms.EditField')),
            ],
        ),
    ]
