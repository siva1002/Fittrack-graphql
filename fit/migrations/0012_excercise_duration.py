# Generated by Django 4.2.6 on 2023-11-10 07:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fit', '0011_alter_trackings_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='excercise',
            name='duration',
            field=models.IntegerField(default=0),
        ),
    ]
