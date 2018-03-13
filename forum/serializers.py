from rest_framework import serializers

from .models import Board, Post, Thread

class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ('name', )