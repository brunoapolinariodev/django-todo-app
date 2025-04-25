from django.test import TestCase
from tasks.models import Task
from django.contrib.auth.models import User

class TaskModelTest(TestCase):
    def test_create_task(self):
        """Cria uma tarefa e verifica os campos"""
        user = User.objects.create_user(username='teste', password='123')
        task = Task.objects.create(
            title='Teste task',
            description='Descrição teste',
            completed=False,
            user=user
        )
        self.assertEqual(task.title, 'Teste task')
        self.assertFalse(task.completed)
