# Generated by Django 4.2.7 on 2023-11-20 22:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='workout_intensity',
            field=models.TextField(choices=[('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High')]),
        ),
    ]
