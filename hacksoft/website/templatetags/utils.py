from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag(takes_context=True)
def full_url(context, url):
    page = context.get('page')

    if page:
        return page.get_site().root_url + url

    return url


@register.simple_tag
def get_from_settings(key, default=None):
    return getattr(settings, key, default)
