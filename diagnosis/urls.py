from django.urls import path
from diagnosis import views

urlpatterns = [
    path('', views.diagnosis, name='diagnosis'),
    path('make_diagnosis/', views.diagnose, name='make_diagnosis'),
]