"""
Tests for custom templatetags and template filters.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.template import Template, Context

from blog.templatetags.blog_extras import author_details


class AuthorDetailsFilterTests(TestCase):
    """
    Test author_details custom template filter.
    """

    def setUp(self):
        self.user = get_user_model().objects.create(
            username='testuser',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )


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
