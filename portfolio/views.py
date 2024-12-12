from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from .forms import RegisterForm
from .models import Portfolio, Skill
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')  
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def dashboard(request):
    portfolio = Portfolio.objects.filter(user=request.user).first()
    skills = Skill.objects.filter(portfolio=portfolio) if portfolio else []
    return render(request, 'users/dashboard.html', {'portfolio': portfolio, 'skills': skills})

@login_required
def delete_skill(request, skill_id):
    skill = get_object_or_404(Skill, id=skill_id, portfolio__user=request.user)
    skill.delete()
    return JsonResponse({'success': True})

@login_required
@require_POST
def add_skill(request):
    portfolio = Portfolio.objects.filter(user=request.user).first()
    if portfolio:
        skill_name = request.POST.get('skill_name')
        skill_description = request.POST.get('skill_description')
        Skill.objects.create(portfolio=portfolio, name=skill_name, description=skill_description)
    return redirect('dashboard')

@login_required
@require_POST
@csrf_exempt
def save_design(request):
    portfolio, created = Portfolio.objects.get_or_create(user=request.user)
    portfolio.accent_color = request.POST.get('accent_color', '')
    portfolio.home_picture = request.POST.get('home_picture', '')
    portfolio.save()
    return redirect('dashboard')

@login_required
@require_POST
@csrf_exempt
def save_about(request):
    portfolio, created = Portfolio.objects.get_or_create(user=request.user)
    portfolio.name = request.POST.get('name', '')
    portfolio.role = request.POST.get('role', '')
    portfolio.about_text = request.POST.get('about_text', '')
    portfolio.linkedin_link = request.POST.get('linkedin_link', '')
    portfolio.save()
    return redirect('dashboard')

@login_required
@require_POST
@csrf_exempt
def save_contact(request):
    request.user.email = request.POST.get('email', '')
    request.user.save()
    return redirect('dashboard')

class CustomLoginView(LoginView):
    template_name = 'users/login.html'

class CustomLogoutView(LogoutView):
    next_page = 'index'