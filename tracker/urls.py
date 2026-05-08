from django.contrib.auth import views as auth_views
from django.urls import path

from . import views
from .forms import LoginForm

urlpatterns = [
    path('', views.splash, name='splash'),
    path('onboarding/', views.onboarding, name='onboarding'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html', authentication_form=LoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('expenses/', views.expense_list, name='expenses'),
    path('expenses/add/', views.expense_create, name='expense_add'),
    path('expenses/<int:pk>/edit/', views.expense_update, name='expense_edit'),
    path('expenses/<int:pk>/delete/', views.expense_delete, name='expense_delete'),
    path('analytics/', views.analytics, name='analytics'),
    path('gamification/', views.gamification, name='gamification'),
    path('reports/', views.reports, name='reports'),
    path('reports/csv/', views.export_csv, name='export_csv'),
    path('reports/pdf/', views.export_pdf, name='export_pdf'),
    path('profile/', views.profile, name='profile'),
]
