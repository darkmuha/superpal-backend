from django.contrib import admin

from .models import Customer, Progress, CustomerTrainingStats

# Register your models here.
admin.site.register(Customer)
admin.site.register(Progress)
admin.site.register(CustomerTrainingStats)
