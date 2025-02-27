from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .serializer import TaskSerializer
from .models import Task


"""
Remember to run the tests to ensure that the API is working as expected.
"""
@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def overview(request):
    """
    Retrieve and return an overview of all tasks.
    This view function handles GET requests to retrieve all tasks from the database.
    It serializes the tasks and returns them in the response along with a message.
    If no tasks are found, it returns a 404 response with an appropriate message.
    Args:
        request (HttpRequest): The HTTP request object.
    Returns:
        Response: A DRF Response object containing the serialized task data and a message.
    """
    """
    You can use get_or_404() method to get the object or return 404 if it does not exist.
    But i want to return a message if no tasks are found.
    """
    try:
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response(
            {
                'message': 'API Overview',
                'data' : serializer.data
            },
            status=status.HTTP_200_OK
        )
    except Task.DoesNotExist:
        return Response(
            {
                'message': 'No tasks found'
            },
            status=status.HTTP_404_NOT_FOUND
        )

@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def create_task(request):
    """
    Handle the creation of a new task.
    This view function handles POST requests to create a new task. It uses the
    TaskSerializer to validate the incoming data. If the data is valid, the task
    is saved and a success response is returned. If the data is invalid, an error
    response is returned.
    Args:
        request (HttpRequest): The HTTP request object containing the task data.
    Returns:
        Response: A DRF Response object containing a success message and the task
                  details if the task is created successfully, or an error message
                  if the data is invalid.
    """
    
    serializer = TaskSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(
            {
                'message': 'Error',
                'data': 'Bad format'
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    else:
        taskData = serializer.validated_data
        serializer.save()
        return Response(
            {
                'message': 'New task has been added',
                'data': {
                    'Task': taskData['title'],
                    'Description': taskData['description']
                }
            },
            status=status.HTTP_201_CREATED
        )

@api_view(['PUT'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def update_task(request):
    """
    Update an existing task with the provided data.
    Args:
        request (HttpRequest): The HTTP request object containing the task data.
    Returns:
        Response: A DRF Response object with a message and data.
            - If the task is not found, returns a 404 response with an error message.
            - If the provided data is not valid, returns a 400 response with an error message.
            - If the task is successfully updated, returns a 200 response with a success message and the updated task data.
    Raises:
        Task.DoesNotExist: If the task with the provided ID does not exist.
    """
    
    try:
        task = Task.objects.get(id=request.data['id'])
    except Task.DoesNotExist:
            return Response(
                {
                    'message': 'Error',
                    'data': 'Task not found'
                },
                status=status.HTTP_404_NOT_FOUND
            )
        
    serializer = TaskSerializer(task, data=request.data, partial=True)
    if not serializer.is_valid():
        return Response(
            {
                'message': 'Error',
                'data': 'Bad format',
                'debug': serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    else:
        taskData = serializer.validated_data
        serializer.save()
        return Response(
            {
                'message': 'Task has been updated',
                'data': serializer.data
            },
            status=status.HTTP_200_OK
        )

@api_view(['DELETE'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def delete_task(request):
    """
    Deletes a task based on the provided task ID in the request data.
    Args:
        request (HttpRequest): The HTTP request object containing the task ID in the request data.
    Returns:
        Response: A Response object with a success message and HTTP 204 status code if the task is deleted successfully.
                  A Response object with an error message and HTTP 404 status code if the task is not found.
    """
    
    try:
        task = Task.objects.get(id=request.data['id'])
        task.delete()
        return Response(
            {
                'message': 'Task has been deleted'
            },
            status=status.HTTP_204_NO_CONTENT
        )
    except Task.DoesNotExist:
        return Response(
            {
                'message': 'Error',
                'data': 'Task not found'
            },
            status=status.HTTP_404_NOT_FOUND
        )
