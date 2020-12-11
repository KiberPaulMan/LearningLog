"""Определяет схемы URL для learning_logs."""
from django.conf.urls import url
from . import views


urlpatterns = [
    # Домашнаяя страница
    url(r'^$', views.index, name='index'),
]
