# Generated by Django 3.2 on 2023-09-30 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0011_auto_20230930_2051'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='rating',
            field=models.FloatField(default=0),
        ),
    ]
