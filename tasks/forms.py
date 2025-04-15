from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'priority', 'completed']

    PRIORITY_CHOICES = [
        ('baixa', 'Baixa'),
        ('media', 'Média'),
        ('alta', 'Alta'),
    ]

    # Adicionando o campo de prioridade
    priority = forms.ChoiceField(choices=PRIORITY_CHOICES, required=True)

    # Adicionando o campo de data limite
    due_date = forms.DateTimeField(required=False, widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
