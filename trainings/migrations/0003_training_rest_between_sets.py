# Generated by Django 4.2.7 on 2023-12-04 22:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trainings', '0002_training_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='training',
            name='rest_between_sets',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
    ]
