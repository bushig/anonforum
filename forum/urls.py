from django.contrib import admin
from django.urls import path

from .views import IndexPage, ThreadList

urlpatterns = [
   path('', IndexPage.as_view(), name='index'),
   path('<str:board>/', ThreadList.as_view(), name='thread-list'),
]
