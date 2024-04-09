from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User

from .models import Task, Label


# Create your tests here.

class LabelModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser')
        self.label = Label.objects.create(name='testlabel', owner=self.user)

    def test_label_creation(self):
        self.assertEqual(self.label.name, 'testlabel')
        self.assertEqual(self.label.owner, self.user)


class TaskModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser')
        self.label = Label.objects.create(name='testlabel', owner=self.user)
        self.task = Task.objects.create(title='testtask', description='testdescription', owner=self.user)
        self.task.labels.add(self.label)

    def test_task_creation(self):
        self.assertEqual(self.task.title, 'testtask')
        self.assertEqual(self.task.description, 'testdescription')
        self.assertEqual(self.task.owner, self.user)
        self.assertEqual(self.task.labels.first(), self.label)


class LabelViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(username='testuser')
        self.client.force_authenticate(user=self.user)
        self.label = Label.objects.create(name='testlabel', owner=self.user)

    def test_label_list(self):
        response = self.client.get('/api/v1/labels/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 1)

    def test_label_retrieve(self):
        response = self.client.get(f'/api/v1/labels/{self.label.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'testlabel')

    def test_label_update(self):
        response = self.client.put(f'/api/v1/labels/{self.label.id}/', {'name': 'updatedlabel'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'updatedlabel')

    def test_label_delete(self):
        response = self.client.delete(f'/api/v1/labels/{self.label.id}/')
        self.assertEqual(response.status_code, 204)


class TaskViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(username='testuser')
        self.client.force_authenticate(user=self.user)
        self.label = Label.objects.create(name='testlabel', owner=self.user)
        self.task = Task.objects.create(title='testtask', description='testdescription', owner=self.user)
        self.task.labels.add(self.label)

    def test_task_list(self):
        response = self.client.get('/api/v1/tasks/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 1)

    def test_task_retrieve(self):
        response = self.client.get(f'/api/v1/tasks/{self.task.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title'], 'testtask')

    def test_task_update(self):
        response = self.client.put(f'/api/v1/tasks/{self.task.id}/', {'title': 'updatedtask', 'description': 'updateddescription', 'labels': [self.label.id]})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title'], 'updatedtask')

    def test_task_delete(self):
        response = self.client.delete(f'/api/v1/tasks/{self.task.id}/')
        self.assertEqual(response.status_code, 204)
