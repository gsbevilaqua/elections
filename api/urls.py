from django.urls import path
from . import views

urlpatterns = [
    path('api/get_results', views.get_results),
    path('api/create_candidates', views.create_candidates),
    path('api/create_voters', views.create_voters),
    path('api/sort_ranks', views.sort_ranks)
]