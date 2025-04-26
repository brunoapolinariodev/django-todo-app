from django.test import TestCase
from tasks.forms import TaskForm
from datetime import datetime

class TaskFormTest(TestCase):

    def test_valid_form(self):
        """Testa se o formulário é válido com dados corretos"""
        form_data = {
            'title': 'Comprar pão',
            'description': 'Ir na padaria às 8h',
            'priority': 'baixa',
            'completed': False,
            'due_date': ''  # ou uma data válida, como '2025-05-01T08:00'
        }
        form = TaskForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        """Testa se o formulário é inválido quando não há título"""
        form_data = {
            'title': '',
            'description': 'Sem título',
            'priority': 'media',
            'completed': False
        }
        form = TaskForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)
