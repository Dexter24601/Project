# Generated by Django 3.2.5 on 2023-01-13 11:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('HadirApp', '0013_absence_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='absence',
            name='date',
        ),
        migrations.AddField(
            model_name='absence',
            name='info',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='HadirApp.attendance'),
        ),
    ]
