"""
Tests for models.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model

from blog import models


def create_user(email='user@example.com', password='testpass123'):
    """
    Create and return a new user.
    """
    return get_user_model().objects.create_user(email, password)


def create_post(**params):
    """
    Create and return a new post.
    """
    user = create_user()
    defaults = {
        'title': 'Example Post',
        'summary': 'Example post summary.',
        'content': 'Example post content',
    }
    defaults.update(params)
    return models.Post.objects.create(author=user, **params)


def create_tag():
    """
    Create and return a new tag.
    """
    return models.Tag.objects.create(value="Test tag")


class ModelTests(TestCase):
    """
    Test models.
    """

    def test_create_post(self):
        """
        Test creating a post is successful.
        """
        post = create_post()

        self.assertEqual(str(post), post.title)

    def test_create_tag(self):
        """
        Test creating a tag is successful.
        """
        tag = create_tag()

        self.assertEqual(str(tag), tag.value)

    def test_create_post_with_tag(self):
        """
        Test creating a post with tag is successful.
        """
        tag = create_tag()
        post = create_post()
        post.tags.add(tag)

        self.assertEqual(str(post), post.title)
        self.assertEqual(post.tags.count(), 1)
