# from django.conf.urls import url 
from django.urls import path, include
from .views import TodoListAPIView, TodoDetailAPIView

urlpatterns = [
    path('api', TodoListAPIView.as_view()),
    path('api/<int:todo_id>/', TodoDetailAPIView.as_view())
]