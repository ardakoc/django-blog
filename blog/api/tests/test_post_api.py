"""
Tests for post api.
"""
from datetime import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone
from pytz import UTC
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from blog.models import Post


class PostApiTestCase(TestCase):
    def setUp(self):
        self.user1 = get_user_model().objects.create_user(
            email='test@example.com', password='password'
        )
        self.user2 = get_user_model().objects.create_user(
            email='test2@example.com', password='password2'
        )
        posts = [
            Post.objects.create(
                author=self.user1,
                published_at=timezone.now(),
                title='Post 1 Title',
                slug='post-1-slug',
                summary='Post 1 Summary',
                content='Post 1 Content',
            ),
            Post.objects.create(
                author=self.user2,
                published_at=timezone.now(),
                title='Post 2 Title',
                slug='post-2-slug',
                summary='Post 2 Summary',
                content='Post 2 Content',
            ),
        ]

        # let us look up the post info by ID
        self.post_lookup = {post.id: post for post in posts}

        self.client = APIClient()
        token = Token.objects.create(user=self.user1)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    def test_post_list(self):
        response = self.client.get('/api/v1/posts')
        data = response.json()
        self.assertEqual(len(data), 2)

        for post_dict in data:
            post = self.post_lookup[post_dict['id']]
            self.assertEqual(post.title, post_dict['title'])
            self.assertEqual(post.slug, post_dict['slug'])
            self.assertEqual(post.summary, post_dict['summary'])
            self.assertEqual(post.content, post_dict['content'])
            self.assertTrue(
                post_dict['author'].endswith(f'/api/v1/users/{post.author.email}')
            )
            self.assertEqual(
                post.published_at,
                datetime.strptime(
                    post_dict['published_at'], '%Y-%m-%dT%H:%M:%S.%fZ'
                ).replace(tzinfo=UTC)
            )
