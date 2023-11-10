from django.contrib import admin
from .models import (User,Workouts,Trackings,Excercise)

# Register your models here.
admin.site.register(User)
admin.site.register(Workouts)
admin.site.register(Trackings)
admin.site.register(Excercise)
