"""
Tests for custom templatetags and template filters.
"""
from django.test import TestCase, Client
from django.contrib.auth import get_user_model, get_user
from django.template import Template, Context
from django.urls import reverse

from blog.templatetags.blog_extras import author_details, recent_posts
from blog.models import Post


class AuthorDetailsFilterTests(TestCase):
    """
    Test author_details custom template filter.
    """

    def setUp(self):
        self.user = get_user_model().objects.create(
            username='testuser',
            first_name='Test',
            last_name='User'
        )
        self.user.set_password('testpass123')
        self.user.save()

    def test_author_details_with_first_and_last_name(self):
        """
        Test the filter on an author that has first and last name.
        """
        self.assertEqual(author_details(self.user), 'Test User')

    def test_author_details_with_username(self):
        """
        Test the filter on an author that does not have
        first and last name.
        """
        user = get_user_model().objects.create(
            username='testuser1',
            password='testpass123',
        )

        self.assertEqual(author_details(user), 'testuser1')

    def test_author_details_with_non_user(self):
        """
        Test the filter with a non-user object.
        """
        non_user = 'Not a user object'

        self.assertEqual(author_details(non_user,), '')

    def test_author_details_template_usage(self):
        """
        Test the filter in a template.
        """
        template = Template('{% load blog_extras %}{{ user|author_details }}')
        context = Context({'user': self.user})
        rendered = template.render(context)

        self.assertEqual(rendered, 'Test User')

    def test_author_details_if_current_user(self):
        """
        Test the filter if author is current user.
        """
        client = Client()
        client.login(username='testuser', password='testpass123')
        response = client.get(reverse('home'))
        current_user = get_user(client)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            author_details(current_user, current_user),
            '<strong>me</strong>'
        )


class RecentPostsTests(TestCase):
    """
    Test recent_posts custom template tag.
    """

    def setUp(self):
        self.user = get_user_model().objects.create(
            username='testuser',
            first_name='Test',
            last_name='User'
        )
        self.post = Post.objects.create(
            author=self.user,
            title='Test Post',
            content='Test Content'
        )

    def test_current_post_excluded(self):
        """
        Test current post is excluded from recent posts list.
        """
        Post.objects.create(author=self.user, title='Another post 1')
        Post.objects.create(author=self.user, title='Another post 2')
        rendered = recent_posts(self.post)

        self.assertNotIn(str(self.post), str(rendered))
        self.assertEqual(len(rendered), 2)
        self.assertEqual(Post.objects.all().count(), 3)
