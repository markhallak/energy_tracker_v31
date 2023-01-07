from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name="question_index"),
    path('<int:id>/', views.details, name="question_detail"),

] 