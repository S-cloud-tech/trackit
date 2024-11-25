from django.urls import path
from . import views

urlpatterns = [
    path( '', views.home ,name='home'),
    path('signup/', views.signup, name='sign_up'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'), 
    path('profile/', views.profile, name='profile'),
    path('profile/update/', views.update_profile, name='update_profile'),
]
