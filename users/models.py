from django.db import models 
from django.contrib.auth.models import  AbstractBaseUser, BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import date

class  UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:raise ValueError("Users must have email address!")
        user= self.model( email= self.normalize_email(email))
        user.set_password(password)
        user.save(using=self.db)
        return user
    def create_superuser(self, email,  password=None ):
        user=self.create_user( email, password=password)
        user.is_admin=True
        user.save(using= self.db)
        return user


class User(AbstractBaseUser):
    email= models.EmailField (
        verbose_name= ' email address', 
        max_length= 255,
        unique= True
    )
    is_active= models.BooleanField(default=True)
    staff= models.BooleanField( default = False)
    is_admin= models.BooleanField( default= False)
    username = models.CharField( max_length=30, unique= True)
   
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects=UserManager()
    def __str__(self):
       return self.email
    
    def has_perm(self, perm, obj=None ):
        return True
    def has_module_perms(self, app_label):
        return True
    @property
    def is_staff(self):
        return self.is_admin
    

class Goal(models.Model):
         
    title = models.CharField(max_length=30)
    description = models.TextField(max_length=255)
    cover_image=models.ImageField(upload_to='static/images', blank=True, null=True)
   

    def __str__(self):
        return self.title
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100, null=True, blank=True)
    date_of_birth= models.DateField(null=True, blank=True)
    gender= models.CharField(max_length=10, null=True, blank=True)
    weight = models.FloatField(null=True, blank=True)
    height = models.FloatField(null=True, blank=True)
    goals = models.ForeignKey(Goal, on_delete=models.CASCADE, null=True, blank=True)
    profile_image = models.ImageField(upload_to='uploads/profiles/', blank=True, null=True)

    def __str__(self):
        return f"Profile of {self.user.email}"

    @property
    def bmi(self):
        if self.weight and self.height:
            height_in_meters = self.height / 100
            return round(self.weight / (height_in_meters ** 2), 2)
        return None
    @property
    def age(self):
        if self.date_of_birth:
            today = date.today()
            return today.year - self.date_of_birth.year - (
                (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
            )
        return None
    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
            