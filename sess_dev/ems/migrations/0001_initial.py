# Generated by Django 2.0.3 on 2018-08-21 13:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='EmpProfile',
            fields=[
                ('emp_id', models.IntegerField(primary_key=True, serialize=False, verbose_name='Employee ID')),
                ('emp_dob', models.DateField(verbose_name='Date of Birth')),
                ('emp_doj', models.DateField(verbose_name='Date of Joining')),
                ('emp_dot', models.DateField(verbose_name='Date of Termination')),
                ('emp_con_primary', models.CharField(max_length=10, verbose_name='Primary contact number')),
                ('emp_con_secondary', models.CharField(max_length=10, verbose_name='Secondary contact number')),
                ('emp_designation', models.CharField(max_length=200, verbose_name='Emnployee designation')),
                ('emp_department', models.IntegerField(verbose_name='Employee Department')),
                ('username', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Emp Profile',
                'verbose_name_plural': 'Emp Profile',
                'ordering': ['-emp_id'],
            },
        ),
    ]
