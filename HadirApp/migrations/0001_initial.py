# Generated by Django 3.2.5 on 2023-01-03 14:18

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Class',
            fields=[
                ('class_id', models.CharField(max_length=3, primary_key=True, serialize=False, validators=[django.core.validators.RegexValidator('\\d{3}')])),
                ('class_name', models.CharField(max_length=50)),
                ('instructor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('name', models.CharField(max_length=60)),
                ('student_id', models.CharField(max_length=8, primary_key=True, serialize=False, validators=[django.core.validators.RegexValidator('^(4)(\\d{7})$')])),
                ('student_absence', models.IntegerField(default=0)),
                ('reg_date', models.DateTimeField(auto_now_add=True, verbose_name='date registered')),
                ('classes', models.ManyToManyField(to='HadirApp.Class')),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('img_id', models.AutoField(primary_key=True, serialize=False)),
                ('images', models.FileField(max_length=300, null=True, upload_to='')),
                ('student', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='HadirApp.student')),
            ],
        ),
    ]
