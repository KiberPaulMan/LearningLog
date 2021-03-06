from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse

from .models import Topic, Entry
from .forms import TopicForm, EntryForm


# Create your views here.


def index(request):
    """Домашняя страница приложения Learning_Log"""
    return render(request, 'learning_logs/index.html')


@login_required
def topics(request):
    """Выводит список тем"""
    obj_topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': obj_topics}
    return render(request, 'learning_logs/topics.html', context)


@login_required
def topic(request, topic_id):
    obj_topic = Topic.objects.get(id=topic_id)
    # Проверка того, что тема принадлежит текущему пользователю.
    if obj_topic.owner != request.user:
        raise Http404
    entries = obj_topic.entry_set.order_by('-date_added')
    context = {'topic': obj_topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)


@login_required
def new_topic(request):
    """Определяет новую тему"""
    if request.method != 'POST':
        # Данные не отправлялись, создается пустная форма
        form = TopicForm()
    else:
        # Отправлены данные POST, обработать данные
        form = TopicForm(request.POST)
        if form.is_valid():
            new_topic_ = form.save(commit=False)
            new_topic_.owner = request.user
            new_topic_.save()
            # form.save()
            return HttpResponseRedirect(reverse('topics'))

    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)


@login_required
def new_entry(request, topic_id):
    """Добавляет новую запись по конкретной теме"""
    topic_obj = Topic.objects.get(id=topic_id)

    if request.method != 'POST':
        # Данные не отправлялись, создается пустная форма
        form = EntryForm()
    else:
        # Отправлены данные POST, обработать данные
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry_obj = form.save(commit=False)
            new_entry_obj.topic = topic_obj
            new_entry_obj.save()
            return HttpResponseRedirect(reverse('topic', args=[topic_id]))

    context = {'topic': topic_obj, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)


@login_required
def edit_entry(request, entry_id):
    """Редактирует существующую запись"""
    entry = Entry.objects.get(id=entry_id)
    topic_obj = entry.topic

    if topic_obj.owner != request.user:
        raise Http404

    if request.method != 'POST':
        # Исходный запрос; форма заполняется данными текущей записи.
        form = EntryForm(instance=entry)
    else:
        # Отправка данных POST; обработать данные.
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('topic', args=[topic_obj.id]))

    context = {'entry': entry, 'topic': topic_obj, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)
