# Generated by Django 4.2.7 on 2024-01-17 06:25

import json
from django.db import migrations, transaction

from trainings.models import Training


@transaction.atomic
def create_initial_data(apps, schema_editor):
    with open('assets/dummy_data/trainings.json', 'r') as file:
        data = json.load(file)

        for training_data in data:
            Training.objects.create(
                name=training_data['name'],
                video=training_data['video'],
                repetitions=training_data['repetitions'],
                sets=training_data['sets'],
                rest_between_sets=training_data['rest_between_sets']
            )


class Migration(migrations.Migration):
    dependencies = [
        ('trainings', '0003_training_rest_between_sets'),
    ]

    operations = [
        migrations.RunPython(create_initial_data)
    ]
