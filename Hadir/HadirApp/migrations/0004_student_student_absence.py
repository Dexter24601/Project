# Generated by Django 3.2.5 on 2023-01-08 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HadirApp', '0003_auto_20230107_1550'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='student_absence',
            field=models.IntegerField(default=0),
        ),
    ]
