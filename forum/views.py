from rest_framework.generics import ListAPIView, ListCreateAPIView
from django.views.generic import TemplateView

from .models import Board, Thread,  Post
from .serializers import BoardSerializer, PostSerializer, ThreadSerializer

# Create your views here.
class IndexPage(TemplateView):
    template_name = 'index.html'