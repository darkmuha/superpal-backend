import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser

from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.html import strip_tags
from django_rest_passwordreset.signals import reset_password_token_created

from authentication.managers import CustomUserManager


# Create your models here.
class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.CharField(max_length=255, unique=True)
    username = models.CharField(max_length=40, unique=True)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()

    def __str__(self):
        return self.username


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    reset_password_url = reset_password_token.key

    email_html_message = render_to_string(
        'password_reset.html',
        {
            'reset_password_url': reset_password_url,
            'title': 'Some website title',
        }
    )
    plaintext_message = strip_tags(email_html_message)

    msg = EmailMultiAlternatives(
        # Subject:
        "Password Reset for Some website title",
        # Message (plain text):
        plaintext_message,
        # From:
        "noreply@somehost.local",
        # To:
        [reset_password_token.user.email]
    )

    msg.attach_alternative(email_html_message, "text/html")

    msg.send()
