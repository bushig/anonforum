from django.db import models
from django.db.models.signals import pre_save, post_save
from django.urls import reverse

# Create your models here.

class Board(models.Model):
    name = models.CharField(max_length=6, unique=True)
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
    bumplimit = models.IntegerField(default=500)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "/{}/ Thread №{}".format(self.board.name, self.number)

    class Meta:
        ordering = ['-is_pinned', '-updated']
    def get_latest_posts(self):
        """
        Returns first post and 3 latest posts.
        """
        result = []
        count = self.post_set.all().count()
        all = self.post_set.all().order_by('-id')
        if count > 0:
            result.append(all[count-1])
        if count > 3:
            all = all[0:3:-1] # TODO: FIX THIS TO HAVE FIRST ENTRY
        elif count == 3:
            all = all[0:2:-1]
        elif count == 2:
            all = all[0:1:-1]
        else:
            all = []
        for post in all:
            result.append(post)
        return result

    def get_absolute_url(self):
        return reverse('thread-view', kwargs={'board':self.board.name, 'thread': self.number})

class MediaFile(models.Model):
    choices = (('jpeg', 'JPEG'),
               ('png', 'PNG'),
               ('webm', 'WEBM'),
               ('mp4', 'MP4'),)
    md5 = models.CharField(max_length=32)
    file = models.ImageField()
    type = models.CharField(choices=choices, max_length=4)
    created = models.DateTimeField(auto_now_add=True)


class Post(models.Model):
    number = models.PositiveIntegerField(blank=True, null=True)
    text = models.CharField(max_length=600)
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    is_OP = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    mediafile = models.ManyToManyField(MediaFile, blank=True)

    def __str__(self):
        return "/{}/ Post №{}".format(self.thread.board.name, self.number)

    def get_absolute_url(self):
        return "/{}/{}#{}".format(self.thread.board.name, self.thread.number, self.number)

def update_thread_or_post_number(sender, instance, *args, **kwargs):
    if instance.number and instance.number != "":
        print(instance.number)
    else:
        if sender == Thread:
            last_record = sender.objects.filter(board=instance.board).last()
        elif sender == Post:
            last_record = sender.objects.filter(thread__board=instance.thread.board).last()
        if last_record:
            instance.number = last_record.number + 1
        else:
            instance.number = 1

def bump_thread(sender, instance, *args, **kwargs):
    thread = instance.thread
    if thread.post_set.count() < thread.bumplimit:
        thread.save() # Should bump

pre_save.connect(update_thread_or_post_number, Thread)
pre_save.connect(update_thread_or_post_number, Post)

post_save.connect(bump_thread, Post)