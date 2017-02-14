from __future__ import unicode_literals
from django.db import models
from django.shortcuts import render, get_object_or_404

from wagtail.wagtailcore import blocks
from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailcore.fields import RichTextField, StreamField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailsnippets.edit_handlers import SnippetChooserPanel
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.contrib.wagtailroutablepage.models import RoutablePageMixin, route
from wagtail.wagtailadmin.edit_handlers import InlinePanel
from modelcluster.fields import ParentalKey

from .snippets import Project, Client, Teammate


class HomePage(Page):
    h1 = models.CharField(max_length=255)
    h2 = models.CharField(max_length=255)

    intro_h1 = models.CharField(max_length=500)
    intro_h2 = models.CharField(max_length=500)
    intro_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    how_we_work_title = models.CharField(max_length=255)
    how_we_work_center = RichTextField()
    how_we_work_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

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

    team_image_main = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    team_image_secondary = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

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
        FieldPanel('h1'),
        FieldPanel('h2'),
        FieldPanel('intro_h1'),
        FieldPanel('intro_h2'),
        ImageChooserPanel('intro_image'),

        FieldPanel('how_we_work_title'),
        FieldPanel('how_we_work_center'),
        ImageChooserPanel('how_we_work_image'),

        FieldPanel('technologies_we_use_title'),
        ImageChooserPanel('technologies_we_use_image'),
        FieldPanel('technologies_we_use_center'),
        InlinePanel('technologies_placement', label="Technologies"),

        FieldPanel('our_team_title'),
        FieldPanel('our_team_center'),
        InlinePanel('teammate_placement', label="Teammates"),
        ImageChooserPanel('team_image_main'),
        ImageChooserPanel('team_image_secondary'),
        FieldPanel('portfolio_title'),
        ImageChooserPanel('portfolio_image'),
        FieldPanel('portfolio_center'),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        context['clients'] = Client.objects.all()
        return context


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
            ('image', ImageChooserBlock()),
            ('title', blocks.RichTextBlock()),
            ('description', blocks.RichTextBlock()),
        ]))
    ])

    the_process_title = RichTextField()

    the_process_content = StreamField([
        ('process_content', blocks.StructBlock([
            ('title', blocks.CharBlock()),
            ('icon_classes', blocks.CharBlock()),
            ('description', blocks.RichTextBlock())
        ], template='streams/process_content.html'))])

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


class PortfolioPage(Page):
    header_text = models.CharField(max_length=255)
    header_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    intro = RichTextField()
    content_panels = Page.content_panels + [
        FieldPanel('header_text'),
        ImageChooserPanel('header_image'),
        FieldPanel('intro'),
        InlinePanel('clients_placement', label="Clients"),
    ]


class ContactsPage(Page):
    header_text = models.CharField(max_length=255)
    header_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    text = RichTextField()
    content_panels = Page.content_panels + [
        FieldPanel('header_text'),
        ImageChooserPanel('header_image'),
        FieldPanel('text'),
    ]


class ProjectPage(RoutablePageMixin, Page):
    @route(r'^([\w-]+)/$')
    def get_project(self, request, slug):
        project = get_object_or_404(Project, slug=slug)
        return render(request, 'website/project_page.html', locals())


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


class ProjectsPlacement(Orderable, models.Model):
    page = ParentalKey('website.HomePage', related_name='projects_placement')
    project = models.ForeignKey('website.Project', related_name='+')

    panels = [
        SnippetChooserPanel('project'),
    ]

    def __str__(self):
        return "{} -> {}".format(self.page.title, self.project.name)


class ClientPlacement(Orderable, models.Model):
    page = ParentalKey('website.PortfolioPage', related_name='clients_placement')
    client = models.ForeignKey('website.Client', related_name='+')

    panels = [
        SnippetChooserPanel('client'),
    ]

    def __str__(self):
        return "{} -> {}".format(self.page.title, self.client.name)


class BlogPostsPage(Page):
    header_text = models.CharField(max_length=255)
    header_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    text = RichTextField()
    content_panels = Page.content_panels + [
        FieldPanel('header_text'),
        ImageChooserPanel('header_image'),
        FieldPanel('text'),
    ]


class BlogPost(Page):
    cover_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    text = models.TextField()
    authors = models.ManyToManyField(Teammate)

    content_panels = Page.content_panels + [
        ImageChooserPanel('cover_image'),
        FieldPanel('text'),
        FieldPanel('authors')
    ]
