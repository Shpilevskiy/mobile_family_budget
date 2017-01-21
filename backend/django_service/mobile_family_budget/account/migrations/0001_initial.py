# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-01-21 21:02
from __future__ import unicode_literals

import account.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BudgetGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('group_owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='RefLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.CharField(max_length=120, unique=True)),
                ('creation_date', models.DateField(default=django.utils.timezone.now)),
                ('expire_date', models.DateField(default=account.models.default_expire_date)),
                ('activation_count', models.PositiveIntegerField(default=3)),
            ],
        ),
        migrations.AddField(
            model_name='budgetgroup',
            name='invite_link',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='account.RefLink'),
        ),
        migrations.AddField(
            model_name='budgetgroup',
            name='users',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
