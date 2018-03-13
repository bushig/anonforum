from django.contrib import admin
from django.urls import path

from .views import ListBoards

urlpatterns = [
   path('', ListBoards.as_view()),
]
