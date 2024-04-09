from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet, LabelViewSet

router = DefaultRouter()
router.register(r'api/v1/tasks', TaskViewSet, basename='tasks')
router.register(r'api/v1/labels', LabelViewSet, basename='labels')

urlpatterns = [
    path('', include(router.urls)),
]
