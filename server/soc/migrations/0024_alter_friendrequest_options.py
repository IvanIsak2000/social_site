# Generated by Django 3.2.8 on 2022-01-02 11:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('soc', '0023_auto_20211231_2253'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='friendrequest',
            options={'ordering': ('-created_at',), 'verbose_name': 'Заявка в друзья', 'verbose_name_plural': 'Заявки в друзья'},
        ),
    ]
