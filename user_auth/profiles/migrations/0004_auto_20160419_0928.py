# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0003_requestapplication'),
    ]

    operations = [
        migrations.AddField(
            model_name='create_opportunity',
            name='starting_time',
            field=models.TimeField(default=datetime.datetime(2016, 4, 19, 9, 28, 2, 909822, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='create_opportunity',
            name='stopping_time',
            field=models.TimeField(default=datetime.datetime(2016, 4, 19, 9, 28, 8, 578940, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
