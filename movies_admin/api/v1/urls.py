from django.urls import path
from api.v1 import views

urlpatterns = [
    path('movies/', views.FilmWorkApi.as_view()),
    path('movies/<str:id>', views.FilmWorkDetailsApi.as_view())
]
