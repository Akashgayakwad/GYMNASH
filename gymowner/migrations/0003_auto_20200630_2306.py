# Generated by Django 3.0.6 on 2020-06-30 23:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gymowner', '0002_auto_20200623_0018'),
    ]

    operations = [
        migrations.AddField(
            model_name='gym',
            name='feature1',
            field=models.CharField(default='feature1', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='gym',
            name='feature2',
            field=models.CharField(default='feature2', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='gym',
            name='feature3',
            field=models.CharField(default='feature3', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='gym',
            name='feature4',
            field=models.CharField(default='feature4', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='gym',
            name='feature5',
            field=models.CharField(default='feature5', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='gym',
            name='original_price',
            field=models.IntegerField(default=1000),
            preserve_default=False,
        ),
    ]