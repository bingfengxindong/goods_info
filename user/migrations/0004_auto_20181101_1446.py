# Generated by Django 2.0.7 on 2018-11-01 14:46

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_auto_20181016_0850'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='create_date',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='userlogintime',
            name='create_date',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
