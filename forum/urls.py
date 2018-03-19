from django.contrib import admin
from django.urls import path

from .views import IndexPage, ThreadList, ThreadView

urlpatterns = [
   path('', IndexPage.as_view(), name='index'),
   path('<str:board>/', ThreadList.as_view(), name='thread-list'),
   path('<str:board>/<int:thread>', ThreadView.as_view(), name='thread-view')
]
