from django.contrib import admin
from django.urls import path

from .views import ListBoards, ListThreads

urlpatterns = [
   path('', ListBoards.as_view()),
   path('<str:board>/', ListThreads.as_view()),
]
