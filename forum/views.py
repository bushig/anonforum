from rest_framework.generics import ListAPIView, ListCreateAPIView
from django.views.generic import TemplateView, View
from django.shortcuts import render, get_object_or_404
from django.http import Http404

from .models import Board, Thread,  Post
from .serializers import BoardSerializer, PostSerializer, ThreadSerializer

# Create your views here.
class IndexPage(View):

    def get(self, request, *args, **kwargs):
        boards = Board.objects.all()
        context = {'boards': boards}
        return render(request, 'index.html', context)

class ThreadList(View):
    def get(self, request, *args, **kwargs):
        board = kwargs.get('board')
        get_object_or_404(Board, name=board)
        threads = Thread.objects.filter(board__name=board, is_archived=False)
        context = {'board': board, 'threads': threads}
        return render(request, 'threads_list.html', context)

class ThreadView(View):
    def get(self):
        pass