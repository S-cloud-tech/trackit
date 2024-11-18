from django.db import models
from users.models import Profile
class WorkoutGroup(models.Model):
    name = models.CharField(max_length=25)
    description = models.TextField(max_length=244)
    related_goals= models.ManyToManyField(to="users.Goal")


    def __str__(self):
        return self.name
    
class Workout(models.Model):
    name= models.CharField(max_length=25)
    image=models.ImageField(upload_to='uploads/workouts', blank=True, null=True)
    workout_group=models.ManyToManyField(to= "WorkoutGroup")
    description = models.TextField()
    duration = models.IntegerField()
    def __str__(self):
        return self.name

class UserWorkoutPlan(models.Model):
    user= models.ForeignKey(Profile, on_delete=models.CASCADE)
    workout = models.ForeignKey('Workout', on_delete=models.CASCADE)
    date_created=models.DateTimeField(auto_now=True)
    completed= models.BooleanField(default=False)

    def __str__(self):
        return self.date_created
    
    

