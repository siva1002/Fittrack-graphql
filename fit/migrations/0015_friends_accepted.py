# Generated by Django 4.2.6 on 2023-11-17 07:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fit', '0014_remove_friends_accepted_friends_requeststatus'),
    ]

    operations = [
        migrations.AddField(
            model_name='friends',
            name='accepted',
            field=models.BooleanField(default=False),
        ),
    ]
