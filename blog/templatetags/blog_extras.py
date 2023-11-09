from django import template
from django.contrib.auth import get_user_model
from django.utils.html import format_html


register = template.Library()


@register.filter
def author_details(author, current_user=None):
    """
    Returns the author's first and last name or username with a
    clickable link refers to their email if exists.
    """
    user_model = get_user_model()

    if not isinstance(author, user_model):
        return ''

    if author == current_user:
        return format_html('<strong>me</strong>')

    if author.first_name and author.last_name:
        name = f'{author.first_name} {author.last_name}'
    else:
        name = f'{author.username}'

    if author.email:
        prefix = format_html(f'<a href="mailto:{author.email}">')
        suffix = format_html('</a>')
    else:
        prefix = ''
        suffix = ''

    return format_html(f'{prefix}{name}{suffix}')


@register.simple_tag
def row(extra_classes=''):
    return format_html(f'<div class="row {extra_classes}">')


@register.simple_tag
def endrow():
    return format_html('</div>')


@register.simple_tag
def col(extra_classes=''):
    return format_html(f'<div class="col {extra_classes}">')


@register.simple_tag
def endcol():
    return format_html('</div>')
