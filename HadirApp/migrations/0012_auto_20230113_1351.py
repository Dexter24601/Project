# Generated by Django 3.2.5 on 2023-01-13 10:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('HadirApp', '0011_auto_20230113_1349'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='absence',
            name='student',
        ),
        migrations.AddField(
            model_name='absence',
            name='student',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='HadirApp.student'),
        ),
    ]