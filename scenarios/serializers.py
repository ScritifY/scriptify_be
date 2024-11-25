from rest_framework import serializers
from movies.models import Genre
from .models import Scenario, Message


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']


class ScenarioSerializer(serializers.ModelSerializer):
    genre = GenreSerializer()
    user = serializers.StringRelatedField()

    class Meta:
        model = Scenario
        fields = ['id', 'genre', 'user', 'created_at']


class MessageSerializer(serializers.ModelSerializer):
    scenario = serializers.PrimaryKeyRelatedField(queryset=Scenario.objects.all())

    class Meta:
        model = Message
        fields = ['id', 'scenario', 'type', 'message_type', 'content', 'created_at']

