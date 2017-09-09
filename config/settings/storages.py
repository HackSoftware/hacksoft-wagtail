from django.conf import settings

from storages.backends.s3boto3 import S3Boto3Storage


class MediaStorage(S3Boto3Storage):
    location = settings.MEDIA_LOCATION


class StaticStorage(S3Boto3Storage):
    location = settings.STATIC_LOCATION
