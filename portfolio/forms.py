from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Portfolio, Skill, SkillPort

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'password1', 'password2', 'name']

class PortfolioForm(forms.ModelForm):
    class Meta:
        model = Portfolio
        fields = ['title', 'description', 'name', 'role', 'linkedin_link', 'me_picture', 'accent_color', 'home_picture']

class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['portfolio', 'name', 'skill_description', 'level']

class SkillPortForm(forms.ModelForm):
    class Meta:
        model = SkillPort
        fields = ['portfolio', 'skill']

class DesignForm(forms.ModelForm):
    class Meta:
        model = Portfolio
        fields = ['accent_color', 'home_picture']

class AboutForm(forms.ModelForm):
    class Meta:
        model = Portfolio
        fields = ['name', 'role', 'linkedin_link', 'me_picture']

class ContactForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']