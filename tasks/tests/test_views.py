from django.test import Client, TestCase
from django.urls import reverse
from tasks.models import Task
from django.contrib.auth.models import User

class ViewTest(TestCase): 
    def setUp(self): 
        self.client = Client()
        self.user = User.objects.create_user(username='teste', password='123')

    def test_homepage_status_code(self): 
      """Verifica se a página inicial responde com status 200"""
      self.client.force_login(self.user)  
      response = self.client.get(reverse('tasks:task_list'))
      self.assertEqual(response.status_code, 200) 

    def test_create_task(self): 
        """Verifica se a tarefa é criada corretamente"""
        data = {
            'title': 'Nova tarefa',
            'description': 'Descrição da nova tarefa',
            'priority': 'baixa',
            'completed': False,
            'user': self.user.id
        }
        self.client.force_login(self.user)
        response = self.client.post(reverse('tasks:add_task'), data)
        self.assertEqual(response.status_code, 302)  # Redireciona após criar
        self.assertEqual(Task.objects.count(), 1)
