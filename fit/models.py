
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
class UserManager(BaseUserManager):
  

  def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
    if not email:
        raise ValueError('Users must have an email address')
    now = timezone.now()
    email = self.normalize_email(email)
    user = self.model(
        email=email,
        is_staff=is_staff, 
        is_active=True,
        is_superuser=is_superuser, 
        last_login=now,
        date_joined=now, 
        **extra_fields
    )
    user.set_password(password)
    user.save(using=self._db)
    return user

  def create_user(self, email, password, **extra_fields):
    return self._create_user(email, password, False, False, **extra_fields)

  def create_superuser(self, email, password, **extra_fields):
    user=self._create_user(email, password, True, True, **extra_fields)
    return user


class User(AbstractBaseUser, PermissionsMixin):
    class Meta:
       db_table="User"
       verbose_name="User"

    email = models.EmailField(max_length=254, unique=True)
    username = models.CharField(max_length=254, null=True, blank=True,unique=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    def get_absolute_url(self):
        return "/users/%i/" % (self.pk)
    
    def __str__(self) -> str:
       return f"{self.username}"
    
class Workouts(models.Model):
   class Meta:
      db_table="Workout"
      verbose_name="Workout"
   user=models.ForeignKey(User, related_name="workouts",on_delete=models.CASCADE)
   name=models.CharField(max_length=50)
   description=models.CharField(max_length=100)

   def __str__(self) -> str:
      return f"{self.name}-{self.description}"

class Excercise(models.Model):
   workout=models.ForeignKey(Workouts,on_delete=models.CASCADE,related_name="exercise")
   exercise=models.CharField(max_length=50)
   sets=models.IntegerField()
   reps=models.IntegerField()

   def __str__(self) -> str:
      return f"{self.exercise}-{self.reps}"
   

class Trackings(models.Model):
   class Meta:
      db_table="Tracking"
      verbose_name="Tracking"
   duration=models.DurationField()
   workout=models.ForeignKey(Workouts, related_name="track", on_delete=models.CASCADE)
   started=models.BooleanField(default=False)
   time=models.DateTimeField(auto_now_add=True)

   def __str__(self) -> str:
        return f"{self.workout}-{self.duration}"

class Friends(models.Model):
   user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="friends")
   userfriend=models.ForeignKey(User,on_delete=models.CASCADE,related_name='user')

   def __str__(self) -> str:
      return f"{self.userfriend} {self.user.username}"
