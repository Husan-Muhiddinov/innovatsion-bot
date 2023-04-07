from django.db import models

# Create your models here.
class UserInformation(models.Model):
    user_id = models.BigIntegerField(null=True)
    first_name = models.CharField(max_length=256, null=True, blank=True)
    last_name = models.CharField(max_length=256, null=True, blank=True)
    username = models.CharField(max_length=256, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user_status=models.BooleanField(default=False, null=True)

    def __str__(self):
        return str(self.first_name)+" " + str(self.last_name)
    
class Department(models.Model):
    name=models.CharField(max_length=200,null=True)

    def __str__(self):
        return self.name

class Ids(models.Model):
    code_id = models.CharField(null=True, max_length=255, unique=True)
    user_id = models.ForeignKey(UserInformation, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    userr=models.ForeignKey(Department,on_delete=models.CASCADE,null=True)
    status=models.CharField(max_length=200,default="Foydalanilmagan", null=True)
    status_ID=models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.code_id
    

class Log(models.Model):
    user_id = models.BigIntegerField(null=True)
    state = models.JSONField(null=True)

