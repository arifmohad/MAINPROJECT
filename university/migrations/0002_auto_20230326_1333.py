# Generated by Django 3.1.5 on 2023-03-26 08:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('university', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='complaint',
            old_name='complaint',
            new_name='postcomplaint',
        ),
        migrations.RemoveField(
            model_name='course',
            name='course_code',
        ),
    ]
