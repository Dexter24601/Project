# Generated by Django 3.2.5 on 2023-01-09 18:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HadirApp', '0009_auto_20230109_2157'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='absence',
            name='student_absence',
        ),
        migrations.AddField(
            model_name='student',
            name='student_absence',
            field=models.IntegerField(default=0),
        ),
    ]
