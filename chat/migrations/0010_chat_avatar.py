# Generated by Django 3.2.8 on 2021-10-27 20:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0009_alter_chat_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='chat',
            name='avatar',
            field=models.ImageField(default=' ', upload_to='media/group_avatars'),
        ),
    ]
