from rest_framework.generics import ListAPIView, ListCreateAPIView
from django.views.generic import TemplateView, View
from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from django.contrib import messages
from django.core.paginator import Paginator
from django.core.files.storage import FileSystemStorage

from .models import Board, Thread, Post
from .forms import CreateThreadForm, MediaUpload


# Create your views here.
class IndexPage(View):
    def get(self, request, *args, **kwargs):
        boards = Board.objects.all()
        context = {'boards': boards}
        return render(request, 'index.html', context)


class ThreadList(View):
    def get(self, request, *args, **kwargs):
        form = CreateThreadForm(request.POST or None)
        upload_forms = MediaUpload()
        board = kwargs.get('board')
        get_object_or_404(Board, name=board)
        threads = Thread.objects.filter(board__name=board, is_archived=False).prefetch_related('board')[:100]  # 10 pages
        paginator = Paginator(threads, 10)
        page = request.GET.get('page', 1)
        threads = paginator.get_page(page)
        context = {'board': board, 'threads': threads, 'form': form, 'upload_forms': upload_forms}
        return render(request, 'threads_list.html', context)

    def post(self, request, *args, **kwargs):
        board = kwargs['board']
        form = CreateThreadForm(request.POST or None)
        upload_forms = MediaUpload(data=request.POST or None, files=request.FILES or None)
        if form.is_valid() and upload_forms.is_valid():
            board = form.cleaned_data['board']
            text = form.cleaned_data['text']
            email = form.cleaned_data['email']
            board_obj = Board.objects.get(name=board)
            thread = Thread.objects.create(board=board_obj, OP=request.META.get('REMOTE_ADDR'))
            upload_forms.save(commit=False)
            # TODO: generate md5 and select image type
            OP_post = Post.objects.create(is_OP=True, text=text, thread=thread)
            if upload_forms.cleaned_data["file"]:
                upload_forms.save()
                OP_post.mediafile.add(upload_forms.instance)
            OP_post.mediafile.add(upload_forms.instance)
            return redirect('thread-view', board=board, thread=thread.number)
        else:
            messages.add_message(request, messages.ERROR, "Didn't created a thread because of errors",
                                 "alert alert-danger")
            return redirect('thread-list', board=board)


class ThreadView(View):
    def get(self, request, *args, **kwargs):
        form = CreateThreadForm(request.POST or None)
        upload_forms = MediaUpload(data=request.POST or None, files=request.FILES or None)
        board = kwargs.get('board')
        thread = kwargs.get('thread')
        posts = Post.objects.filter(thread__number=thread)
        thread = Thread.objects.get(number=thread)
        context = {'posts': posts, 'board': board, 'thread': thread, 'form': form, 'form2': upload_forms}
        return render(request, 'thread.html', context)

    def post(self, request, *args, **kwargs):
        thread = kwargs.get('thread')
        form = CreateThreadForm(request.POST or None)
        upload_forms = MediaUpload(data=request.POST or None, files=request.FILES or None)
        board = kwargs.get('board')
        if form.is_valid() and upload_forms.is_valid():
            board = form.cleaned_data['board']
            text = form.cleaned_data['text']
            email = form.cleaned_data['email']
            is_op = form.cleaned_data['is_op']

            thread = Thread.objects.get(number=thread, board__name=board)
            OP = False
            if is_op and request.META.get('REMOTE_ADDR') == thread.OP:
                OP = True
            post = Post.objects.create(is_OP=OP, text=text, thread=thread)
            if upload_forms.cleaned_data["file"]:
                upload_forms.save()
                post.mediafile.add(upload_forms.instance)
            messages.add_message(request, messages.SUCCESS, 'Successfully posted', "alert alert-success")
            return redirect('thread-view', board=board, thread=thread.number)
        else:
            messages.add_message(request, messages.ERROR, "Didn't created a post because of invalid input.",
                                 "alert alert-danger")
            return redirect('thread-view', board=board, thread=thread)
