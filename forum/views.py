from rest_framework.generics import ListAPIView, ListCreateAPIView
from django.views.generic import TemplateView, View
from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404

from .models import Board, Thread,  Post
from .serializers import BoardSerializer, PostSerializer, ThreadSerializer
from .forms import CreateThreadForm

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

    def post(self, request, *args, **kwargs):
        form = CreateThreadForm(request.POST or None)
        if form.is_valid():
            board = form.cleaned_data['board']
            text = form.cleaned_data['text']
            email = form.cleaned_data['email']
            board_obj = Board.objects.get(name=board)
            thread = Thread.objects.create(board=board_obj, OP=request.META.get('REMOTE_ADDR'))
            OP_post = Post.objects.create(is_OP=True, text=text, thread=thread)
            return redirect('thread-view', board= board, thread = thread.number)

class ThreadView(View):
    def get(self, request, *args, **kwargs):
        board = kwargs.get('board')
        thread = kwargs.get('thread')
        posts = Post.objects.filter(thread__number = thread)
        thread = Thread.objects.get(number=thread)
        context = {'posts': posts, 'board': board, 'thread': thread}
        return render(request, 'thread.html', context)