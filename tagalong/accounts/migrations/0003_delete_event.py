# Generated by Django 3.2.7 on 2022-04-15 19:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_event'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Event',
        ),
    ]
