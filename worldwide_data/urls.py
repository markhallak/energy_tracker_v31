from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="worldwide_data_index"),
    path('getmapdata',views.mydata, name="getmapdata"),
]