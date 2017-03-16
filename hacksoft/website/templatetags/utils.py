from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def full_url(context, url):
    page = context.get('page')

    if page:
        return page.get_site().root_url + url

    return url
