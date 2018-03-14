from rest_framework import serializers

from .models import Board, Post, Thread

class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ('name', )

class ThreadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Thread
        fields = ('number', 'is_pinned', 'is_archived', 'created')

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('number', 'text', 'is_OP', 'created')