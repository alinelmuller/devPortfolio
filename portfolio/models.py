from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email

    def get_portfolio(self):
        return Portfolio.objects.filter(user=self).first()

class Portfolio(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=100, default='Name')
    role = models.CharField(max_length=100, default='Role')
    linkedin_link = models.URLField(default='https://www.linkedin.com')
    me_picture = models.ImageField(upload_to='me_pictures/', default='default_me_picture.jpg')
    accent_color = models.CharField(max_length=7, default='#000')  
    home_picture = models.ImageField(upload_to='home_pictures/', default='default_home_picture.jpg')

    def __str__(self):
        return self.title

class Skill(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    skill_description = models.TextField()
    level = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class SkillPort(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.portfolio.title} - {self.skill.name}"