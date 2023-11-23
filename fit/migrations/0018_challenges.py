# Generated by Django 4.2.6 on 2023-11-23 12:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fit', '0017_alter_workouts_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='Challenges',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('challenge', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='challengeworkout', to='fit.workouts')),
                ('challengeduser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='createdchallenges', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='challenges', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'Challenges',
            },
        ),
    ]
