from django.urls import path, re_path
from . import views

app_name = 'posts'

urlpatterns = [
    path('create/', views.posts_create),
    path('', views.posts_list, name='display'),
]