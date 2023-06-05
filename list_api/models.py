from django.contrib.auth.models import AbstractUser
from django.db import models

# from list_api.managers import CustomUserManager

class CustomUser(AbstractUser):
    first_name = None
    last_name = None
    email = None



    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=255,unique=True,null=False,blank=False, default = "")
    password = models.CharField(max_length=255)


    is_active= models.BooleanField(default=True)
    is_staff= models.BooleanField(default=False)

    REQUIRED_FIELDS = []

    # USERNAME_FIELD = "username"
    # REQUIRED_FIELDS = ['username', "password"]

    # objects = CustomUserManager()

    # email = models.EmailField(max_length=50, unique=True)
    # first_name = models.CharField(max_length=255)
    # last_name = models.CharField(max_length=255)

    # username = models.CharField(max_length=50, unique=True)
    # password = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.username


class UserToken(models.Model):
    user_id = models.IntegerField()
    token = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    expired_at = models.DateTimeField()

    def __str__(self):
        return self.user_id

class Reset(models.Model):
    username = models.CharField(max_length=255)
    token = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.username
    
    

class List(models.Model):
    id = models.AutoField(primary_key=True)
    ownerUserID = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, null=False, blank=False)
    name = models.CharField(max_length=100, null=False, blank=False)

    class Meta:
        unique_together = ['ownerUserID', 'name']

    def __str__(self):
        return self.name


class Task(models.Model):
    id = models.AutoField(primary_key=True)
    ownerListID = models.ForeignKey(
        List, on_delete=models.CASCADE, null=False, blank=False)
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=100)
    data_of_creation = models.DateField(auto_now_add=True)
    is_complete = models.BooleanField(default=False)
    start_date = models.DateTimeField(null=True)
    end_date = models.DateTimeField(null=True)


    def __str__(self):
        return self.title

    class Meta:
        # ordering = ["is_complete"]
        unique_together = ['ownerListID', 'title']


