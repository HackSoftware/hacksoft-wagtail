from django.conf import settings


def django_settings(request):
    return dict(django_settings=settings.SETTINGS_MODULE)
