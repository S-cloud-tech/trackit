from django.contrib import admin
from . models import WorkoutGroup,UserWorkoutPlan,Workout

# Register your models here.
admin.site.register(WorkoutGroup)

admin.site.register(UserWorkoutPlan)


admin.site.register(Workout)