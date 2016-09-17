from __future__ import unicode_literals
from django.db import models

from wagtail.wagtailcore import blocks
from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailcore.fields import RichTextField, StreamField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailsnippets.edit_handlers import SnippetChooserPanel


from wagtail.wagtailadmin.edit_handlers import InlinePanel
from wagtail.wagtailsnippets.models import register_snippet

from modelcluster.fields import ParentalKey


class HomePage(Page):
    intro_h1 = models.CharField(max_length=255)
    intro_h2 = models.CharField(max_length=255)
    intro_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    how_we_work_title = models.CharField(max_length=255)
    how_we_work_center = RichTextField()
    how_we_work_left = RichTextField()
    how_we_work_right = RichTextField()

    technologies_we_use_title = models.CharField(max_length=255)
    technologies_we_use_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    technologies_we_use_center = RichTextField()

    our_team_title = models.CharField(max_length=255)
    our_team_center = RichTextField()

    portfolio_title = models.CharField(max_length=255)
    portfolio_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    portfolio_center = RichTextField()

    content_panels = Page.content_panels + [
        FieldPanel('intro_h1'),
        FieldPanel('intro_h2'),
        ImageChooserPanel('intro_image'),

        FieldPanel('how_we_work_title'),
        FieldPanel('how_we_work_center'),
        FieldPanel('how_we_work_left'),
        FieldPanel('how_we_work_right'),

        FieldPanel('technologies_we_use_title'),
        ImageChooserPanel('technologies_we_use_image'),
        FieldPanel('technologies_we_use_center'),
        InlinePanel('technologies_placement', label="Technologies"),

        FieldPanel('our_team_title'),
        FieldPanel('our_team_center'),
        InlinePanel('teammate_placement', label="Teammates"),

        FieldPanel('portfolio_title'),
        ImageChooserPanel('portfolio_image'),
        FieldPanel('portfolio_center'),
        InlinePanel('projects_placement', label="Projects")
    ]


class HowWeWorkPage(Page):
    header_text = models.CharField(max_length=255)
    header_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    how_we_work_intro = RichTextField()
    what_we_do_title = models.CharField(max_length=255)
    what_we_do_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    what_we_do_content = StreamField([
        ('what_we_do_content', blocks.StreamBlock([
            ('title', blocks.RichTextBlock()),
            ('description', blocks.RichTextBlock())
        ]))
    ])

    the_process_title = RichTextField()
    the_process_content = StreamField([
        ('process_content', blocks.StreamBlock([
            ('title', blocks.RichTextBlock()),
            ('description', blocks.RichTextBlock())
        ]))
    ])
    content_panels = Page.content_panels + [
        FieldPanel('header_text'),
        ImageChooserPanel('header_image'),
        FieldPanel('how_we_work_intro'),
        FieldPanel('what_we_do_title'),
        ImageChooserPanel('what_we_do_image'),
        StreamFieldPanel('what_we_do_content'),
        FieldPanel('the_process_title'),
        StreamFieldPanel('the_process_content'),
    ]


class TechnologiesWeUsePage(Page):
    header_text = models.CharField(max_length=255)
    header_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    technologies_intro = RichTextField()
    content_panels = Page.content_panels + [
        FieldPanel('header_text'),
        ImageChooserPanel('header_image'),
        FieldPanel('technologies_intro'),
        InlinePanel('technologies_placement', label="Technologies"),
    ]


class OurTeamPage(Page):
    header_text = models.CharField(max_length=255)
    header_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    content_panels = Page.content_panels + [
        FieldPanel('header_text'),
        ImageChooserPanel('header_image'),
        InlinePanel('teammate_placement', label="Teammates"),
    ]


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


class TeammatePlacement(Orderable, models.Model):
    page = ParentalKey('website.HomePage', related_name='teammate_placement')
    teammate = models.ForeignKey('website.Teammate', related_name='+')

    panels = [
        SnippetChooserPanel('teammate'),
    ]

    def __str__(self):
        return "{} -> {}".format(self.page.title, self.teammate.name)


class TeammatePagePlacement(Orderable, models.Model):
    page = ParentalKey('website.OurTeamPage', related_name='teammate_placement')
    teammate = models.ForeignKey('website.Teammate', related_name='+')

    panels = [
        SnippetChooserPanel('teammate'),
    ]

    def __str__(self):
        return "{} -> {}".format(self.page.title, self.teammate.name)


class TechnologiesPlacement(Orderable, models.Model):
    page = ParentalKey('website.HomePage', related_name='technologies_placement')
    technology = models.ForeignKey('website.Technology', related_name='+')

    panels = [
        SnippetChooserPanel('technology'),
    ]

    def __str__(self):
        return "{} -> {}".format(self.page.title, self.technology.name)


class TechnologiesPagePlacement(Orderable, models.Model):
    page = ParentalKey('website.TechnologiesWeUsePage', related_name='technologies_placement')
    technology = models.ForeignKey('website.Technology', related_name='+')

    panels = [
        SnippetChooserPanel('technology'),
    ]

    def __str__(self):
        return "{} -> {}".format(self.page.title, self.technology.name)


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
    logo = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    short_index_description = RichTextField()
    description = RichTextField()

    panels = [
        FieldPanel('name'),
        ImageChooserPanel('demo_image'),
        ImageChooserPanel('logo'),
        FieldPanel('description'),
        FieldPanel('short_index_description'),
    ]

    def __str__(self):
        return self.name


class ProjectsPlacement(Orderable, models.Model):
    page = ParentalKey('website.HomePage', related_name='projects_placement')
    project = models.ForeignKey('website.Project', related_name='+')

    panels = [
        SnippetChooserPanel('project'),
    ]

    def __str__(self):
        return "{} -> {}".format(self.page.title, self.project.name)
