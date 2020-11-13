from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from tasks.forms import TaskForm
from django.core.paginator import Paginator
from tasks.models import Task
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import datetime

@login_required
def taskslist(request):

    search = request.GET.get('search') # esse search é do nome do input de busca no html
    filter = request.GET.get('filter')

    if search:
        tasks = Task.objects.filter(title__icontains=search, user=request.user) # filtra e busca quais tasks tem o search

    elif filter:
        tasks = Task.objects.filter(done__icontains=filter, user=request.user)

    else:
        tasks_list = Task.objects.all().order_by('-created').filter(user=request.user)
        paginator = Paginator(tasks_list, 3)
        page = request.GET.get('page')
        tasks = paginator.get_page(page)
    return render(request, 'tasks/list.html', {'tasks': tasks})


@login_required
def yourname(request, name):
    return render(request, 'tasks/yourname.html', {'name': name})


@login_required
def taskView(request, id):
    # Busca o model Task com chave primária = id, q é a que o usuário clica e aparece no link
    task = get_object_or_404(Task, pk=id)
    return render(request, 'tasks/task.html', {'task': task})


@login_required
def newTask(request):
    if request.method == "POST":
        form = TaskForm(request.POST) # Preenchendo o formulário com os dados do POST

        if form.is_valid():
            task = form.save(commit=False) # Para a inserção de dados e espera até q mandamos salvar, até modificar
            task.done = 'doing'
            task.user = request.user # Autenticando novo usuário pra poder adicionar tarefa
            task.save()
            return redirect('/')

    else:
        form = TaskForm()
        return render(request, 'tasks/newtask.html', {'form': form})


@login_required
def editTask(request, id):
    task = get_object_or_404(Task, pk=id)
    form = TaskForm(instance=task) # O instance é pra deixar o form pré-populado pra exibir pro usuário

    if (request.method == 'POST'):
        form = TaskForm(request.POST, instance=task)

        if(form.is_valid()):
            task.save()
            return redirect('/')

        else:
            return render(request, 'tasks/edittask.html', {'form': form, 'task': task})

    else:
       return render(request, 'tasks/edittask.html', {'form': form, 'task': task})


@login_required
def deleteTask(request, id):
    task = get_object_or_404(Task, pk=id)
    task.delete()
    messages.info(request, 'Task deleted!')
    return redirect('/')


@login_required()
def changeStatus(request, id):
    task = get_object_or_404(Task, pk=id)

    if task.done == 'doing':
        task.done = 'done'

    else:
        task.done = 'doing'

    task.save()
    return redirect('/' )


@login_required()
def dashboard(request, id):
    tasks_done_recently = Task.objects.filter(done='done', user=request.user, update_date__gt=datetime.datetime.now()
                                                                       - datetime.timedelta(days=30)).count()
    tasks_done = Task.objects.filter(done='done', user=request.user).count()
    tasks_doing = Task.objects.filter(done='doing', user=request.user).count()

    return render(request, 'tasks/dashboard.html', {'tasks_done_recently': tasks_done_recently,
                                               'tasks_done': tasks_done,
                                               'tasks_doing': tasks_doing})

