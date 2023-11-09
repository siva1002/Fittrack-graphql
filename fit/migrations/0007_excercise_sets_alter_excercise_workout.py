# Generated by Django 4.2.6 on 2023-10-17 11:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fit', '0006_rename_excercise_excercise_exercise'),
    ]

    operations = [
        migrations.AddField(
            model_name='excercise',
            name='sets',
            field=models.IntegerField(default=2),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='excercise',
            name='workout',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='exercise', to='fit.workouts'),
        ),
    ]
