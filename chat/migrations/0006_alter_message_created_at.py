# Generated by Django 3.2.7 on 2021-10-22 09:13

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0005_alter_message_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 22, 9, 13, 8, 453517)),
        ),
    ]
