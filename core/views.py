from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from .models import Task
from .serializers import TaskSerializer
from .serializers import RegisterSerializer
from django.contrib.auth.models import User

def home(request):
    return HttpResponse("Hello, Django!")

@api_view (["GET"])
@permission_classes([IsAuthenticated])
def tasks_collection(request):

    queryset = Task.objects.filter(owner=request.user)
    
    #optional
    search = request.query_params.get("search")
    if search:
        from django.db.models import Q
        queryset = queryset.filter(Q(title__icontains=search) | Q(description__icontains=search))
        
    #optional
    ordering = request.query_params.get("ordering")
    allowed = {"created_at", "updated_at", "due_date"}
    if ordering in allowed:
        queryset = queryset.order_by(ordering)
    else:
        queryset = queryset.order_by("-created_at")
    
    paginator = PageNumberPagination()
    page = paginator.paginate_queryset(queryset, request)
    if page is not None:
        serializer = TaskSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)
    serializer = TaskSerializer(queryset, many=True)
    return Response(serializer.data)

@api_view (["POST"])                    # each function needs its own decorator
@permission_classes([IsAuthenticated])  # Auth required for POST
def create_task(request):
    serializer = TaskSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(owner=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view (["PUT"])
@permission_classes([IsAuthenticated])  # Auth required for PUT
def update_task(request, pk):
    try:
        task = Task.objects.get(pk=pk)
    except Task.DoesNotExist:
        return Response({"error":"Task not found"}, status=status.HTTP_404_NOT_FOUND)
    
    if task.owner != request.user:
        return Response({"error":"you don't have permission to update this task"}, status=status.HTTP_403_FORBIDDEN)
    
    serializer = TaskSerializer(task, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK) 
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view (["DELETE"])
@permission_classes([IsAuthenticated]) # Auth required for DELETE
def delete_task(request, pk):
    try:
        task = Task.objects.get(pk=pk)
    except Task.DoesNotExist:
        return Response({"error":"Task not found"}, status=status.HTTP_404_NOT_FOUND)
    
    if task.owner != request.user:
        return Response({"error":"you don't have permission to delete this task"}, status=status.HTTP_403_FORBIDDEN)
    
    task.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(["POST"])
@permission_classes([AllowAny])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message" : "User created successfully"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


