from django.db import models


# Create your models here.

class Board(models.Model):
    name = models.CharField(max_length=6)
    bump_limit = models.IntegerField(default=500)
    thread_limit = models.IntegerField(default=50)

    def __str__(self):
        return "/{}/".format(self.name)


class Thread(models.Model):
    number = models.IntegerField()
    is_pinned = models.BooleanField(default=False)
    is_archived = models.BooleanField(default=False)
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    OP = models.GenericIPAddressField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Thread №{}".format(self.number)


class Post(models.Model):
    number = models.IntegerField()
    text = models.CharField(max_length=600)
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    is_OP = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Post №{}".format(self.number)