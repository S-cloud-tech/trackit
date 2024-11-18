from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from .forms import LoginForm,ProfileForm
from .models import Profile
from .admin import  UserCreationForm
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings



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
            print("Form is valid")

            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
           
            if user:
                print("auth")
                login(request, user)    
                return redirect('dashboard')
        else:
            print("not auth")
            form = LoginForm()
            print(login)
    else:
        print("Form errors:",form.errors)
              

    return render(request, 'login.html',{'form':form})
def profile(request):
    user=request.user
    
    return render(request, 'profile.html',{'user':user})

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

@login_required
def update_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)  

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')  
        form = ProfileForm(instance=profile)

    return render(request, 'profile_update.html', {'form': form})