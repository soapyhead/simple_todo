# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-07-25 05:07
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='company',
            options={'ordering': ('name',), 'verbose_name': 'company', 'verbose_name_plural': 'companies'},
        ),
    ]