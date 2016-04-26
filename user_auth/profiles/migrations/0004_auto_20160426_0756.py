# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('profiles', '0003_delete_profile'),
    ]

    operations = [
        migrations.CreateModel(
            name='Willing_Hour',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('hours', models.IntegerField(default=0)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='dated',
            name='hours',
        ),
        migrations.AddField(
            model_name='dated',
            name='time',
            field=models.TimeField(default=datetime.datetime(2016, 4, 26, 7, 56, 39, 887018, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
