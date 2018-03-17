from django.db import models
from django.db.models.signals import pre_save

# Create your models here.

class Board(models.Model):
    name = models.CharField(max_length=6)
    bump_limit = models.IntegerField(default=500)
    thread_limit = models.IntegerField(default=50)

    def __str__(self):
        return "/{}/".format(self.name)


class Thread(models.Model):
    number = models.PositiveIntegerField(blank=True, null=True)
    is_pinned = models.BooleanField(default=False)
    is_archived = models.BooleanField(default=False)
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    OP = models.GenericIPAddressField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Thread №{}".format(self.number)


class Post(models.Model):
    number = models.PositiveIntegerField(blank=True, null=True)
    text = models.CharField(max_length=600)
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    is_OP = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Post №{}".format(self.number)

def update_thread_or_post_number(sender, instance, *args, **kwargs):
    if instance.number and instance.number != "":
        print(instance.number)
    else:
        if sender == Thread:
            last_record = sender.objects.filter(board=instance.board).last()
        elif sender == Post:
            last_record = sender.objects.filter(thread=instance.thread).last()
        if last_record:
            instance.number = last_record.number + 1
        else:
            instance.number = 1


pre_save.connect(update_thread_or_post_number, Thread)
pre_save.connect(update_thread_or_post_number, Post)