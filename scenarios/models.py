from django.db import models
from movies.models import Genre
from accounts.models import User


# Create your models here.
class Scenario(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name='scenarios')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='scenarios')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Scenario {self.id} by {self.user.username}"
    

class Message(models.Model):
    MESSAGE_TYPE_CHOICES = [
        ('request', 'Request'),
        ('response', 'Response'),
    ]
    MESSAGE_SUBTYPE_CHOICES = [
        ('first', 'First'),
        ('revise', 'Revise'),
        ('line', 'Line'),
        ('detail', 'Detail'),
    ]

    scenario = models.ForeignKey(Scenario, on_delete=models.CASCADE, related_name='messages')
    type = models.CharField(max_length=10, choices=MESSAGE_TYPE_CHOICES)
    message_type = models.CharField(max_length=10, choices=MESSAGE_SUBTYPE_CHOICES)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.type.capitalize()} - {self.message_type.capitalize()}"
