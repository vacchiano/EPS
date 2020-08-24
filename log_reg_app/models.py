from django.db import models
import re
import bcrypt


# Create your models here.




class UserManager(models.Manager):
    def basic_validator(self, post_data):
        
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        password = post_data['password']
        password_confirm = post_data['confirm']


        if len(post_data['first_name'])<2:
            errors['first_name'] = 'First name must be at least 2 characters long'
        if len(post_data['last_name'])<2:
            errors['last_name'] = 'Last name must be at least 2 characters long'
        if len(post_data['password'])<8:
            errors['password'] = 'Password must be at least 8 characters long'
        if not EMAIL_REGEX.match(post_data['email']):               
            errors['email'] = ("Invalid email address!")
        if password != password_confirm:
            errors['password'] = 'Passwords do not match'
        return errors

    def login(self, post_data):
        from .models import User
        errors = {}

        all_users = User.objects.all()
        

        username_post = post_data['username']
        password_post = post_data['password']

        for user in all_users:
            if username_post == user.email and bcrypt.checkpw(password_post.encode(), user.password.encode())==True:
                errors = {}
                return errors
            
            if username_post != user.email or password_post != user.password:
                errors['password'] = 'Email/Password incorrect'


        return errors



    


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    password = models.TextField()
    user_lvl = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    # work_days
    # points
    # daily_reports

class Work_Day(models.Model):
    date = models.DateTimeField()
    clock_in = models.DateTimeField(auto_now_add=True)
    clock_out = models.DateTimeField(auto_now=True)
    total_time = models.IntegerField()
    desc = models.TextField()
    user = models.ForeignKey(User, related_name='work_days', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # points_earned
    # daily_report

class Points(models.Model):
    total_pts = models.IntegerField()
    user = models.ForeignKey(User, related_name='total_points', on_delete=models.CASCADE)
    work_day = models.ForeignKey(Work_Day, related_name='points_earned', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Daily_Report(models.Model):
    recipients = models.EmailField()
    challenges = models.TextField()
    help_to_give = models.TextField()
    user = models.ForeignKey(User, related_name='daily_reports', on_delete=models.CASCADE)
    work_day = models.ForeignKey(Work_Day, related_name='daily_report', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)