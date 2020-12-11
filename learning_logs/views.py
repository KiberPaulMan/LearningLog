from django.shortcuts import render
from .models import Topic
# Create your views here.


def index(request):
    """Домашняя страница приложения Learning_Log"""
    return render(request, 'learning_logs/index.html')


def topics(request):
    """Выводит список тем"""
    obj_topics = Topic.objects.order_by('date_added')
    context = {'topics': obj_topics}
    return render(request, 'learning_logs/topics.html', context)


def topic(request, topic_id):
    obj_topic = Topic.objects.get(id=topic_id)
    entries = obj_topic.entry_set.order_by('-date_added')
    context = {'topic': obj_topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)
