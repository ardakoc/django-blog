from django.contrib.auth import get_user_model
from django import template


register = template.Library()


@register.filter
def author_details(author):
    """
    Returns the author's first and last name, or username.
    """
    user_model = get_user_model()
    
    if not isinstance(author, user_model):
        return ''
    
    if author.first_name and author.last_name:
        return f'{author.first_name} {author.last_name}'
    return f'{author.username}'
