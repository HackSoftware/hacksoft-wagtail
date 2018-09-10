from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

from wagtail.core import blocks
from wagtail.core.fields import RichTextField, StreamField
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.models import register_snippet


@register_snippet
class Teammate(models.Model):
    name = models.CharField(max_length=255)
    description = RichTextField()
    initial_photo = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    secondary_photo = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    panels = [
        FieldPanel('name'),
        ImageChooserPanel('initial_photo'),
        ImageChooserPanel('secondary_photo'),
        FieldPanel('description')
    ]

    def __str__(self):
        return self.name


@register_snippet
class Technology(models.Model):
    name = models.CharField(max_length=255)
    logo = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    description = RichTextField()

    panels = [
        FieldPanel('name'),
        ImageChooserPanel('logo'),
        FieldPanel('description')
    ]

    def __str__(self):
        return self.name


@register_snippet
class Client(models.Model):
    name = models.CharField(max_length=255)
    description = RichTextField()
    logo = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    panels = [
        FieldPanel('name'),
        ImageChooserPanel('logo'),
        FieldPanel('description'),
    ]

    def __str__(self):
        return self.name


@register_snippet
class Project(models.Model):
    name = models.CharField(max_length=255)
    client = models.ForeignKey(Client, null=True, blank=True)

    description = RichTextField()

    demo_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    technologies = models.ManyToManyField(Technology)
    panels = [
        FieldPanel('name'),
        ImageChooserPanel('demo_image'),
        FieldPanel('description'),
        FieldPanel('client'),
        FieldPanel('technologies'),
    ]

    def __str__(self):
        return self.name


@register_snippet
class Footer(models.Model):
    links_text = models.CharField(max_length=255)
    contact_text = models.CharField(max_length=255)
    button_text = models.CharField(max_length=255)
    popup_text = RichTextField()
    popup_heading = models.CharField(max_length=255)

    links = StreamField([
        ('link', blocks.StructBlock([
            ('text', blocks.TextBlock()),
            ('url', blocks.URLBlock()),
        ], template='streams/footer_link.html'))
    ])

    panels = [
        FieldPanel('links_text'),
        FieldPanel('contact_text'),
        FieldPanel('button_text'),
        FieldPanel('popup_text'),
        FieldPanel('popup_heading'),
        StreamFieldPanel('links'),
    ]

    def __str__(self):
        return self.links_text


@register_snippet
class Category(models.Model):
    name = models.CharField(max_length=55)

    panels = [
        FieldPanel('name'),
    ]

    def __str__(self):
        return self.name


@register_snippet
class HackCastEpisode(models.Model):
    title = models.CharField(unique=True, max_length=255)
    description = models.TextField(blank=True)

    mp3_url = models.URLField()
    youtube_url = models.URLField()

    duration = models.PositiveIntegerField(
        default=0,
        help_text='Duration of the episode in minutes'
    )

    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title
