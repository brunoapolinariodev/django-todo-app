# tasks/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Task
from .forms import TaskForm
from django.http import JsonResponse

@login_required
def task_list(request):
    status = request.GET.get('status', 'todas')
    ordenar = request.GET.get('ordenar', 'created_at')

    if status == 'pendentes':
        tasks = Task.objects.filter(user=request.user, completed=False)
        titulo = "Tarefas Pendentes"
    elif status == 'concluidas':
        tasks = Task.objects.filter(user=request.user, completed=True)
        titulo = "Tarefas Concluídas"
    else:
        tasks = Task.objects.filter(user=request.user)
        titulo = "Minhas Tarefas"

    if ordenar == 'nome':
        tasks = tasks.order_by('title')
    elif ordenar == 'prioridade':
        prioridade_ordem = {'alta': 0, 'media': 1, 'baixa': 2}
        tasks = sorted(tasks, key=lambda x: prioridade_ordem[x.prioridade])
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
        return JsonResponse({'success': True, 'completed': task.completed})
    return JsonResponse({'success': False}, status=400)


