"""Определяет схемы URL для learning_logs."""
from django.conf.urls import url
from . import views


urlpatterns = [
    # Домашнаяя страница
    url(r'^$', views.index, name='index'),
    url(r'^topics/$', views.topics, name='topics'),
    # Страница с подробной информацией по отдельной теме
    url(r'^topics/(?P<topic_id>\d+)/$', views.topic, name='topic')
]
