# Generated by Django 3.2.8 on 2021-12-24 20:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('soc', '0015_auto_20211220_2004'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='groupchat',
            name='token',
        ),
    ]
