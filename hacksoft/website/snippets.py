from __future__ import unicode_literals
from wagtail.wagtailsnippets.models import register_snippet
from django.db import models


from wagtail.wagtailcore import blocks
from wagtail.wagtailcore.fields import RichTextField, StreamField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel


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
class Project(models.Model):
    name = models.CharField(max_length=255)
    demo_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    cover_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    slug = models.SlugField()
    logo = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    video = models.FileField(null=True, blank=True)
    short_index_description = RichTextField()
    description = RichTextField()

    long_description = StreamField([
        ('paragraph', blocks.StructBlock([
            ('text', blocks.RichTextBlock())
        ], template='streams/project_description_paragraph.html'))])

    panels = [
        FieldPanel('name'),
        FieldPanel('slug'),
        FieldPanel('video'),
        FieldPanel('cover_image'),
        ImageChooserPanel('demo_image'),
        ImageChooserPanel('logo'),
        FieldPanel('description'),
        StreamFieldPanel('long_description'),
        FieldPanel('short_index_description'),
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
        ],
        template='streams/footer_link.html'))
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
