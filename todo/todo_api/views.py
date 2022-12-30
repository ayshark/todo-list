from django.shortcuts import render
# from django.contrib.auth import get_user_model

from rest_framework.views import APIView
from rest_framework import permissions, status
from .models import Todo
from .serializers import TodoSerializer
from rest_framework.response import Response


class TodoListAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated] #check if the useris authenticated or not

    #List view
    def get(self, request):
        todos = Todo.objects.filter(user = request.user.id)
        serializer = TodoSerializer(todos, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)


    def post(self, request):
        data = {
            'task': request.data.get('task'),
            'status': request.data.get('status'),
            'user': request.user.id
        }

        serializer = TodoSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)


class TodoDetailAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, todo_id, user_id):
        """ helper method to get the object with given todo_id and user_id"""
        try:
            return Todo.objects.get(id = todo_id, user = user_id)
        except Todo.DoesNotExist:
            return None

    def get(self, request, todo_id):
        # this method retrieves todo instance with the given todo_id
        todo_instance = self.get_object(todo_id, request.user.id)
        if not todo_instance:
            return Response(
                {'res': 'Object does not exist'},
                status = status.HTTP_400_BAD_REQUEST
            )
        serializer = TodoSerializer(todo_instance)
        return Response(serializer.data, status = status.HTTP_200_OK)

    def delete(self, request, todo_id):
        todo_instance = self.get_object(todo_id, request.user.id)
        if not todo_instance:
            return Response(
                {'res': 'Object does not exist'},
                status = status.HTTP_400_BAD_REQUEST
            )
        todo_instance.delete()
        return Response(
            {'res': 'Task deleted'},
            status = status.HTTP_200_OK
        )

    def put(self, request, todo_id):
        todo_instance = self.get_object(todo_id, request.user.id)
        if not todo_instance:
            return Response(
                {'res': 'object does not exist'},
                status = status.HTTP_400_BAD_REQUEST
            )
        data = {
            'task': request.data.get('task'),
            'status': request.data.get('status'),
            'user': request.user.id
        }
        serializer = TodoSerializer(instance = todo_instance, data = data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status = status.HTTP_200_OK
            )
        return Response(
            serializer.errors,
            status = status.HTTP_400_BAD_REQUEST
        )

        