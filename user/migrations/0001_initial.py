# Generated by Django 3.0.6 on 2020-05-29 19:54

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import user.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='GymUser',
            fields=[
                ('phone', models.CharField(max_length=15, unique=True, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in format '+99999999' up to 14 digits", regex='^\\+?1?\\d{9,14}$')])),
                ('u_id', models.AutoField(primary_key=True, serialize=False)),
                ('fname', models.CharField(blank=True, max_length=20, null=True, verbose_name='First Name')),
                ('lname', models.CharField(blank=True, max_length=20, null=True, verbose_name='Last Name')),
                ('email', models.CharField(blank=True, max_length=40, null=True, verbose_name='Email Address')),
                ('dob', models.DateField(blank=True, null=True, verbose_name='Date Of Birth')),
                ('sex', models.CharField(blank=True, max_length=6, null=True)),
                ('first_login', models.BooleanField(default=True)),
                ('timestamp', models.DateField(auto_now_add=True)),
                ('city', models.ForeignKey(default=user.models.get_default_city, on_delete=django.db.models.deletion.CASCADE, to='user.City')),
            ],
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='OTP',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('otp', models.IntegerField()),
                ('count', models.IntegerField(default=1)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.GymUser')),
            ],
        ),
        migrations.AddField(
            model_name='city',
            name='state',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.State'),
        ),
    ]
