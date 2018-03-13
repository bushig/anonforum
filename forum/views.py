from django.shortcuts import render

from rest_framework.generics import ListAPIView

from .models import Board
from .serializers import BoardSerializer

# Create your views here.
class ListBoards(ListAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer