# Generated by Django 3.2.7 on 2021-10-22 09:10

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0003_auto_20211021_1638'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 22, 9, 10, 59, 352191)),
        ),
    ]
