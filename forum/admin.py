from django.contrib import admin

from .models import Board, Post, Thread

class PostsAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        return self.readonly_fields + ('number', )

class ThreadsAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        return self.readonly_fields + ('number',)

# Register your models here.
admin.site.register(Board)
admin.site.register(Post, PostsAdmin)
admin.site.register(Thread, ThreadsAdmin)