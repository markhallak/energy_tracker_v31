from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('home/', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='user_profile'),
    path('dashboard/', auth_views.LoginView.as_view(template_name='dashboard.html'), name='dashboard_index')
    
    # path('user_index/', views.user_index, name='user_list'),
    # path('user_detail/', views.user_detail, name='user_detail'),
] 