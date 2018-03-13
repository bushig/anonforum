from django.db import models

# Create your models here.

class Post(models.Model):

    text = models.CharField(max_length=600)
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    is_OP = models.BooleanField(default=False)

class Thread(models.Model):
    is_pinned = models.BooleanField(default=False)
    is_archived = models.BooleanField(default=False)
    board = models.ForeignKey(Board, on_delete=models.CASCADE)

class Board(models.Model):
    name = models.CharField(max_length=6)
