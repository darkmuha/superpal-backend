from django.contrib import admin
from django.urls import path, include

import workouts

urlpatterns = [
    path('admin/', admin.site.urls),
    path('workouts/', include('workouts.urls')),
    path('trainings/', include('trainings.urls')),
    path('customers/', include('customers.urls')),
    path('authentication/', include('authentication.urls')),
    path('superpals/', include('superpals.urls'))
]
