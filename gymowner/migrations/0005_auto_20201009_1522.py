# Generated by Django 3.0.6 on 2020-10-09 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gymowner', '0004_auto_20200703_0225'),
    ]

    operations = [
        migrations.AddField(
            model_name='gym',
            name='eight_monthly_price',
            field=models.IntegerField(default=-1),
        ),
        migrations.AddField(
            model_name='gym',
            name='eleven_monthly_price',
            field=models.IntegerField(default=-1),
        ),
        migrations.AddField(
            model_name='gym',
            name='five_monthly_price',
            field=models.IntegerField(default=-1),
        ),
        migrations.AddField(
            model_name='gym',
            name='four_monthly_price',
            field=models.IntegerField(default=-1),
        ),
        migrations.AddField(
            model_name='gym',
            name='nine_monthly_price',
            field=models.IntegerField(default=-1),
        ),
        migrations.AddField(
            model_name='gym',
            name='seven_monthly_price',
            field=models.IntegerField(default=-1),
        ),
        migrations.AddField(
            model_name='gym',
            name='six_monthly_price',
            field=models.IntegerField(default=-1),
        ),
        migrations.AddField(
            model_name='gym',
            name='ten_monthly_price',
            field=models.IntegerField(default=-1),
        ),
        migrations.AddField(
            model_name='gym',
            name='three_monthly_price',
            field=models.IntegerField(default=-1),
        ),
        migrations.AddField(
            model_name='gym',
            name='twelve_monthly_price',
            field=models.IntegerField(default=-1),
        ),
        migrations.AddField(
            model_name='gym',
            name='two_monthly_price',
            field=models.IntegerField(default=-1),
        ),
    ]
