from typing import TypeVar, Generic

from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, pagination, permissions, status
from rest_framework.response import Response

from .models import Task, Label
from .serializers import TaskSerializer, LabelSerializer


# Create your views here.


class DefaultPagination(pagination.PageNumberPagination):
    """
    Pagination class with default pagination settings
    """
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000


class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to view and edit it.
    """
    def has_object_permission(self, request, view, obj):
        """
        Return True if permission is granted, False otherwise.
        """
        return obj.owner == request.user


class BaseViewSet(viewsets.ModelViewSet):
    pagination_class = DefaultPagination
    permission_classes = [IsOwner]
    filter_backends = [DjangoFilterBackend, OrderingFilter]

    def get_queryset(self):
        """
        :return: Return queryset for current owner.
        """
        return self.model.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        """
        Override this method to set the owner as the current user.
        :param serializer: the serializer of the Model.
        """
        serializer.save(owner=self.request.user)


class LabelViewSet(BaseViewSet):
    model = Label
    serializer_class = LabelSerializer
    filterset_fields = ['id', 'name']
    ordering_fields = ['id', 'name']


class TaskViewSet(BaseViewSet):
    model = Task
    serializer_class = TaskSerializer
    filterset_fields = ['id', 'title', 'completion_status', 'labels']
    ordering_fields = ['id', 'title', 'completion_status', 'labels']

