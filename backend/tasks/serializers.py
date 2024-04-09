from rest_framework import serializers
from .models import Task, Label


class LabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Label
        fields = ['id', 'name', 'owner']
        read_only_fields = ['owner']


class TaskSerializer(serializers.ModelSerializer):
    labels = serializers.PrimaryKeyRelatedField(many=True, queryset=Label.objects.all())

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'completion_status', 'owner', 'labels']
        read_only_fields = ['owner']

    def create(self, validated_data):
        labels_data = validated_data.pop('labels')
        task = Task.objects.create(**validated_data)
        for label_data in labels_data:
            task.labels.add(label_data)
        return task
