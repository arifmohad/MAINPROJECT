# Generated by Django 3.1.5 on 2023-03-29 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('university', '0002_auto_20230326_1333'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='father_name',
            field=models.CharField(default=223, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='student',
            name='mother_name',
            field=models.CharField(default=2, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='student',
            name='regno',
            field=models.CharField(default=22, max_length=100),
            preserve_default=False,
        ),
    ]
