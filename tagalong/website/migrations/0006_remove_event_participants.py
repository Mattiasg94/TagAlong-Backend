# Generated by Django 3.2.7 on 2022-04-15 21:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0005_event_participants'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='participants',
        ),
    ]