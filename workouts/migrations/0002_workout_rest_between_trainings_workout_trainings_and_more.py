# Generated by Django 4.2.7 on 2023-11-20 22:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trainings', '0001_initial'),
        ('workouts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='workout',
            name='rest_between_trainings',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='workout',
            name='trainings',
            field=models.ManyToManyField(to='trainings.training'),
        ),
        migrations.AlterField(
            model_name='workout',
            name='intensity',
            field=models.TextField(choices=[('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High')]),
        ),
        migrations.DeleteModel(
            name='WorkoutTraining',
        ),
    ]