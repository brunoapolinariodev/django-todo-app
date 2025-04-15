# tasks/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Task
from .forms import TaskForm
from django.http import JsonResponse
from django.db import models

@login_required
def task_list(request):
    status = request.GET.get('status', 'todas')
    ordenar = request.GET.get('ordenar', 'created_at')

    # Filtrando por status
    if status == 'pendentes':
        tasks = Task.objects.filter(user=request.user, completed=False)
        titulo = "Tarefas Pendentes"
    elif status == 'concluidas':
        tasks = Task.objects.filter(user=request.user, completed=True)
        titulo = "Tarefas Concluídas"
    else:
        tasks = Task.objects.filter(user=request.user)
        titulo = "Minhas Tarefas"

    # Ordenando por critérios
    if ordenar == 'nome':
        tasks = tasks.order_by('title')
    elif ordenar == 'prioridade':
        prioridade_ordem = {'alta': 0, 'media': 1, 'baixa': 2}
        tasks = tasks.annotate(priority_order=models.Case(
            models.When(priority='alta', then=models.Value(0)),
            models.When(priority='media', then=models.Value(1)),
            models.When(priority='baixa', then=models.Value(2)),
            default=models.Value(3),
            output_field=models.IntegerField(),
        )).order_by('priority_order')
    else:
        tasks = tasks.order_by('-created_at')

    return render(request, 'tasks/task_list.html', {
        'tasks': tasks,
        'status': status,
        'ordenar': ordenar,
        'titulo': titulo
    })


@login_required
def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('tasks:task_list')
    else:
        form = TaskForm()
    return render(request, 'tasks/task_form.html', {'form': form})

@login_required
def edit_task(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('tasks:task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/task_form.html', {'form': form})

@login_required
def delete_task(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks:task_list')
    return render(request, 'tasks/confirm_delete.html', {'task': task})

@login_required
def toggle_complete(request, pk):
    if request.method == 'POST':
        task = get_object_or_404(Task, pk=pk, user=request.user)
        task.completed = not task.completed
        task.save()
        return JsonResponse({'success': True, 'completed': task.completed}, status=200)
    return JsonResponse({'success': False}, status=400)



