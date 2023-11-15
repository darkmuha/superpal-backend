# Generated by Django 4.2.7 on 2023-11-15 23:55

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Training',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('video', models.CharField(max_length=255)),
                ('repetitions', models.PositiveIntegerField()),
                ('sets', models.PositiveIntegerField()),
            ],
        ),
    ]
