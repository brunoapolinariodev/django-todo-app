from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    PRIORITY_CHOICES = [
        ('baixa', 'Baixa'),
        ('media', 'Média'),
        ('alta', 'Alta'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    due_date = models.DateTimeField(null=True, blank=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='baixa')
    completed = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)  # Adicionando o campo de data de criação

    def __str__(self):
        return self.title
