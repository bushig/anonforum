from django.contrib import admin
from django.urls import path

from .views import IndexPage, ThreadList

urlpatterns = [
   path('', IndexPage.as_view()),
   path('<str:board>/', ThreadList.as_view()),
]
