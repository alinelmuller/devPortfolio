from django.urls import path, include
from . import views
from .views import CustomLoginView, CustomLogoutView

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('delete-skill/<int:skill_id>/', views.delete_skill, name='delete_skill'),
    path('save_design/', views.save_design, name='save_design'),
    path('save_about/', views.save_about, name='save_about'),
    path('save_contact/', views.save_contact, name='save_contact'),
    path('add-skill/', views.add_skill, name='add_skill'),
    path('portfolio/<int:pk>/', views.portfolio_detail, name='portfolio_detail'),
    path('me/', views.user_portfolio, name='user_portfolio'),
    path('send_message/', views.send_message, name='send_message'),
]