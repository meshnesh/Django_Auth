# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
from django.conf import settings
import django.core.validators
import location_field.models.plain


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AcceptedRequests',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='Create_opportunity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', models.ImageField(default=0, upload_to='static/image', verbose_name='My Photo', blank=True)),
                ('title', models.CharField(max_length=140)),
                ('location', models.CharField(max_length=255)),
                ('coordinates', location_field.models.plain.PlainLocationField(max_length=63)),
                ('description', models.TextField(null=True)),
                ('hours_required', models.CharField(max_length=140, blank=True)),
                ('starting_time', models.TimeField()),
                ('stopping_time', models.TimeField()),
                ('starting_date', models.DateField()),
                ('stopping_date', models.DateField()),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Dated',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField()),
                ('hours', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('docfile', models.FileField(upload_to='documents/%Y/%m/%d')),
            ],
        ),
        migrations.CreateModel(
            name='profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=1200)),
                ('description', models.TextField(default='description default')),
            ],
        ),
        migrations.CreateModel(
            name='RequestApplication',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('requests', models.ForeignKey(to='profiles.Create_opportunity')),
            ],
        ),
        migrations.CreateModel(
            name='SimplePlace',
            fields=[
                ('user', models.OneToOneField(primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('distance_away', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('location', models.CharField(max_length=255)),
                ('coordinates', location_field.models.plain.PlainLocationField(max_length=63)),
            ],
        ),
        migrations.CreateModel(
            name='Skills',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('skill', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='UserSkills',
            fields=[
                ('user', models.OneToOneField(primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('skills', models.ManyToManyField(to='profiles.Skills')),
            ],
        ),
        migrations.AddField(
            model_name='requestapplication',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='dated',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='create_opportunity',
            name='skills',
            field=models.ManyToManyField(to='profiles.Skills'),
        ),
        migrations.AddField(
            model_name='create_opportunity',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='acceptedrequests',
            name='requests',
            field=models.ForeignKey(to='profiles.Create_opportunity'),
        ),
        migrations.AddField(
            model_name='acceptedrequests',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
