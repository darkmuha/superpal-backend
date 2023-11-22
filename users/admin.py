from django.contrib import admin

from .models import User, Customer, Progress, UserTrainingStats

# Register your models here.
admin.site.register(User)
admin.site.register(Customer)
admin.site.register(Progress)
admin.site.register(UserTrainingStats)
