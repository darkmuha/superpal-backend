from django.contrib import admin

from .models import SuperPals, SuperPalWorkoutRequest

# Register your models here.
admin.site.register(SuperPals)
admin.site.register(SuperPalWorkoutRequest)
