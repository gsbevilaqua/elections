from django.urls import path
from . import views

urlpatterns = [
    path('api/get_results', views.get_results)
]