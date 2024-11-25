from rest_framework import serializers
from .models import Review

class ReviewSerializer(serializers.ModelSerializer):
    reviewId = serializers.IntegerField(source='id', read_only=True)
    userId = serializers.IntegerField(source='user.id', read_only=True)
    userName = serializers.StringRelatedField(source='user.name', read_only=True)

    class Meta:
        model = Review
        fields = ['reviewId', 'userId', 'userName', 'content', 'rank', 'created_at']
