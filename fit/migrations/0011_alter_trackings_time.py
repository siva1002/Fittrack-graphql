# Generated by Django 4.2.6 on 2023-11-10 06:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fit', '0010_alter_trackings_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trackings',
            name='time',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
