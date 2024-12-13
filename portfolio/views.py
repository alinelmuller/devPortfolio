from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from .forms import RegisterForm, PortfolioForm, SkillForm, SkillPortForm, DesignForm, AboutForm, ContactForm
from .models import Portfolio, Skill, SkillPort
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings
from django.contrib import messages

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
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.portfolio = request.user.get_portfolio()
            skill.save()
            return redirect('dashboard')
    return redirect('dashboard')

@login_required
@require_POST
@csrf_exempt
def save_design(request):
    if request.method == 'POST':
        form = DesignForm(request.POST, request.FILES, instance=request.user.get_portfolio())
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    return redirect('dashboard')

@login_required
@require_POST
@csrf_exempt
def save_about(request):
    if request.method == 'POST':
        form = AboutForm(request.POST, request.FILES, instance=request.user.get_portfolio())
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    return redirect('dashboard')

@login_required
@require_POST
@csrf_exempt
def save_contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    return redirect('dashboard')

def portfolio_detail(request, pk):
    portfolio = get_object_or_404(Portfolio, pk=pk)
    skills = Skill.objects.filter(portfolio=portfolio)
    skill_ports = SkillPort.objects.filter(portfolio=portfolio)
    return render(request, 'portfolio/portfolio_detail.html', {'portfolio': portfolio, 'skills': skills, 'skill_ports': skill_ports})

# def user_portfolio(request):
#     portfolio = get_object_or_404(Portfolio, user=request.user)
#     skills = Skill.objects.filter(portfolio=portfolio)
#     return render(request, 'me/user_portfolio.html', {'portfolio': portfolio, 'skills': skills})


@login_required
def user_portfolio(request):
    portfolio, created = Portfolio.objects.get_or_create(
        user=request.user,
        defaults={
            'title': 'Default Title',
            'description': 'Default Description',
            'name': 'Default Name',
            'role': 'Default Role',
            'linkedin_link': 'https://www.linkedin.com',
            'me_picture': 'default_me_picture.jpg',
            'accent_color': '#000000',
            'home_picture': 'default_home_picture.jpg',
        }
    )
    skills = Skill.objects.filter(portfolio=portfolio)
    return render(request, 'me/user_portfolio.html', {'portfolio': portfolio, 'skills': skills})

@login_required
def send_message(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        message = request.POST['message']
        subject = f"Message from {name} via DevPortfolio"
        full_message = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
        send_mail(subject, full_message, settings.DEFAULT_FROM_EMAIL, [request.user.email])
        return redirect(reverse('user_portfolio'))
    return render(request, 'me/user_portfolio.html')

class CustomLoginView(LoginView):
    template_name = 'users/login.html'

class CustomLogoutView(LogoutView):
    next_page = 'index'


def send_message(request):
    if request.method == 'POST':
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        from_email = request.POST.get('from_email')
        recipient_list = ['recipient-email@example.com']

        try:
            send_mail(subject, message, from_email, recipient_list)
            messages.success(request, 'Email sent successfully.')
        except Exception as e:
            messages.error(request, f'Error sending email: {e}')

    return redirect('some_view_name')