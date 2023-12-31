# Generated by Django 4.2.7 on 2023-11-15 23:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('superpals', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='superpalworkoutrequest',
            name='recipient_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipient_requests', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='superpalworkoutrequest',
            name='sender_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sender_requests', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='superpals',
            name='favorite_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='superpals_favorite_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='superpals',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='superpals_user', to=settings.AUTH_USER_MODEL),
        ),
    ]
