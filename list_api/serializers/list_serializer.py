from rest_framework import serializers
from list_api.models import List, Task


class ListSerializer(serializers.ModelSerializer):
    class Meta:
        model = List
        fields = "__all__"

        extra_kwargs = {
            'ownerUserID': {'write_only': True}
        }


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"
