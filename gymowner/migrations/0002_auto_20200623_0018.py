# Generated by Django 3.0.6 on 2020-06-23 00:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gymowner', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='gym',
            old_name='price',
            new_name='monthly_price',
        ),
        migrations.AddField(
            model_name='gym',
            name='daily_price',
            field=models.IntegerField(default=100),
            preserve_default=False,
        ),
    ]
