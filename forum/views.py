from rest_framework.generics import ListAPIView, ListCreateAPIView
from django.views.generic import TemplateView, View
from django.shortcuts import render

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
        if board:
            threads = Thread.objects.filter(board__name=board, is_archived=False)
            context = {'board': board, 'threads': threads}
            return render(request, 'threads_list.html', context)
        else:
            pass #TODO: 404 page