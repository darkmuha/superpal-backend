# Generated by Django 4.2.7 on 2023-11-15 23:55

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('trainings', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Workout',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=40, unique=True)),
                ('difficulty', models.TextField(choices=[('Beginner', 'Beginner'), ('Intermediate', 'Intermediate'), ('Pro', 'Pro')])),
                ('intensity', models.TextField(choices=[('Low', 'Low'), ('Medium', 'Medium'), ('HIGH', 'High')])),
            ],
        ),
        migrations.CreateModel(
            name='WorkoutTraining',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('training_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trainings.training')),
                ('workout_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workouts.workout')),
            ],
        ),
    ]
