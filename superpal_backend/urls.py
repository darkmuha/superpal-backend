from django.contrib import admin
from django.urls import path, include

import workouts

urlpatterns = [
    path('admin/', admin.site.urls),
    path('workouts/', include('workouts.urls')),
]
