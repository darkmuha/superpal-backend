from django.contrib import admin
from django.urls import path, include

import workouts

urlpatterns = [
    path('admin/', admin.site.urls),
    path('workouts/', include('workouts.urls')),
    path('trainings/', include('trainings.urls')),
    path('customers/', include('users.urls')),
    path('auth/', include('auth.urls'))
]
