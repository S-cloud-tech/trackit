from django.shortcuts import render
import random
from datetime import date
from .models import Workout, WorkoutGroup,UserWorkoutPlan
from django.http import JsonResponse
 

def generate_daily_workout(user):
    """
    Generates a personalized workout for the user based on their profile data.
    """
    # Fetch user profile
    profile = user.profile  # Assuming a OneToOneField relation from User to Profile

    # Determine workout intensity based on user's BMI or goals
    if profile.bmi < 18.5:
        intensity = "low"
    elif 18.5 <= profile.bmi < 25:
        intensity = "medium"
    else:
        intensity = "high"

    # Fetch workouts matching intensity
    matching_workouts = Workout.objects.filter(intensity=intensity)

    # Shuffle and select a random subset of workouts
    selected_workouts = random.sample(list(matching_workouts), min(3, len(matching_workouts)))

    # Create a daily plan
    daily_plan = {
        "date": date.today(),
        "workouts": [
            {
                "name": workout.name,
                "category": workout.category.name,
                "description": workout.description,
                "duration": workout.duration,
            }
            for workout in selected_workouts
        ],
    }
    return daily_plan



def mark_workout_completed(request, workout_id):
    if request.user.is_authenticated:
        try:
            daily_workout = DailyWorkout.objects.get(id=workout_id, user=request.user)
            daily_workout.completed = True
            daily_workout.save()
            return JsonResponse({"success": True, "message": "Workout marked as completed."})
        except DailyWorkout.DoesNotExist:
            return JsonResponse({"success": False, "message": "Workout not found."})
    return JsonResponse({"success": False, "message": "User not authenticated."})


# Create your views here.
