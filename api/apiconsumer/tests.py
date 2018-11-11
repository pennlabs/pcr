"""
Test for the API views.
"""

from django.test import TestCase
from django.test.client import Client

from api.apiconsumer.models import APIConsumer
from api.courses.models import Department


class NoTokenTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_no_token_should_403(self):
        response = self.client.get('/depts/')
        self.assertEqual(response.status_code, 403, response.request)

    def test_invalid_token_should_403(self):
        response = self.client.get('/depts/', {'token': 'token'})
        self.assertEqual(response.status_code, 403, response.request)


class Permission0Test(TestCase):
    def setUp(self):
        self.consumer = APIConsumer.objects.create(
            name="test",
            email="test@test.com",
            description="",
            token="root",
            permission_level=0
        )
        self.client = Client()

    def test_valid_token_should_403(self):
        response = self.client.get('/depts/', {'token': self.consumer.token})
        self.assertEqual(response.status_code, 403, response.request)


class Permission1Test(TestCase):
    def setUp(self):
        self.consumer = APIConsumer.objects.create(
            name="test",
            email="test@test.com",
            description="",
            token="root",
            permission_level=1
        )
        self.client = Client()

    def test_valid_token_should_not_403(self):
        response = self.client.get('/depts/', {'token': self.consumer.token})
        self.assertNotEqual(response.status_code, 403, response.request)
