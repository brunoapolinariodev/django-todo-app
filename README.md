# Django To-Do App

Aplicação web construída com Django que permite aos usuários autenticados gerenciar suas tarefas.

## Recursos

- Login e logout com autenticação Django
- Lista de tarefas por usuário
- Interface responsiva com Bootstrap 5
- Separação por namespaces de URL
- Boas práticas com uso de `@login_required` e arquivos organizados

## Como executar

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```
