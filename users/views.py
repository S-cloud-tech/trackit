from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from .forms import LoginForm,ProfileForm
from .models import Profile
from .admin import  UserCreationForm


def home(request):
    return render(request, 'home.html')

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

              
def logout_view(request):
       logout(request)
       return redirect('/')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user = authenticate.login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})
def login(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user:
                login(request, user)    
                return redirect('dashboard')
        else:
            form = LoginForm()
    
    return render(request, 'login.html',{'form':form})
def user_profile(request):
    user=request.user
    bmi= user.bmi
    return render(request, 'user_profile.html',{'user':user,'bmi':bmi})
@login_required
def profile_update(request):
    # Get the current user's profile or create one if it doesn't exist
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile_update')  # Redirect after successful submission
    else:
        form = ProfileForm(instance=profile)
    
    return render(request, 'profile_update.html', {'form': form})