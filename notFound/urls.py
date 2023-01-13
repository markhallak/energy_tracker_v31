from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="notFound_index"),
]