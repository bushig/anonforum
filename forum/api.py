from rest_framework.generics import ListAPIView, ListCreateAPIView

from .models import Board, Thread,  Post
from .serializers import BoardSerializer, PostSerializer, ThreadSerializer

# Create your views here.
class ListBoards(ListAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer

class ListThreads(ListCreateAPIView):
    queryset = Thread.objects.filter(is_archived=False)
    serializer_class = ThreadSerializer

    def get_queryset(self):
        board = self.kwargs.get('board')
        if board:
            return Thread.objects.filter(board__name=board)
        else:
            return Thread.objects.none()
