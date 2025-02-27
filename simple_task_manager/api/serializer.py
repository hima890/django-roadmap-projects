from rest_framework import serializers
from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    """
    Serializer for the Task model.
    This serializer converts Task model instances to and from JSON format.
    It includes all fields of the Task model.
    Attributes:
        Meta (class): Meta options for the TaskSerializer.
            model (Task): The model that this serializer is for.
            fields (str): Specifies that all fields in the model should be included in the serialization.
    """
    
    class Meta:
        model = Task
        fields = '__all__'
