# Generated by Django 3.2.5 on 2023-01-24 19:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HadirApp', '0010_alter_class_creation_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='traning',
            name='id',
        ),
        migrations.AddField(
            model_name='traning',
            name='img_id',
            field=models.AutoField(default=0, primary_key=True, serialize=False),
            preserve_default=False,
        ),
    ]
