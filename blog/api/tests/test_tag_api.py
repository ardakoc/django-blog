"""
Tests for tag api.
"""
from django.contrib.auth import get_user_model
from django.test import LiveServerTestCase
from rest_framework.test import RequestsClient

from blog.models import Tag


class TagApiTestCase(LiveServerTestCase):
    def setUp(self):
        get_user_model().objects.create_user(
            email='test@example.com', password='password'
        )
        
        self.tag_values = {"tag1", "tag2", "tag3", "tag4"}
        for value in self.tag_values:
            Tag.objects.create(value=value)
        self.client = RequestsClient()

    def test_tag_list(self):
        response = self.client.get(self.live_server_url + '/api/v1/tags/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 4)
        self.assertEqual(self.tag_values, {tag['value'] for tag in data})
