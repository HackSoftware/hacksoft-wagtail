from __future__ import unicode_literals
import operator
from django.db import models
from django.shortcuts import render, get_object_or_404

from wagtail.core import blocks
from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField, StreamField
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.images.blocks import ImageChooserBlock
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.admin.edit_handlers import InlinePanel
from modelcluster.fields import ParentalKey, ParentalManyToManyField

from .snippets import Project, Client, Teammate, Category, HackCastEpisode


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
        context['clients'] = Client.objects.select_related('logo')
        context['technologies'] = TechnologiesPlacement.objects.select_related(
            'technology', 'technology__logo'
        )
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

    subpage_types = []
    parent_page_types = ['website.HomePage']


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

    subpage_types = []
    parent_page_types = ['website.HomePage']


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

    subpage_types = []
    parent_page_types = ['website.HomePage']

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request)

        select = ['teammate', 'teammate__initial_photo', 'teammate__secondary_photo']
        prefetch = []

        context['teammates'] = TeammatePagePlacement.objects.select_related(*select).prefetch_related(*prefetch)

        return context


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

    subpage_types = []
    parent_page_types = ['website.HomePage']

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request)

        select = ['client', 'client__logo', 'page']
        prefetch = [
            'client__project_set',
            'client__project_set__technologies',
            'client__project_set__technologies__logo'
        ]

        context['clients'] = ClientPlacement.objects.select_related(*select).prefetch_related(*prefetch)
        return context


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

    subpage_types = []
    parent_page_types = ['website.HomePage']


class ProjectPage(RoutablePageMixin, Page):
    subpage_types = []
    parent_page_types = ['website.HomePage']

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
    featured_article = models.OneToOneField(
        'BlogPost',
        blank=True,
        null=True,
        related_name='+',
        on_delete=models.SET_NULL)

    content_panels = Page.content_panels + [
        FieldPanel('header_text'),
        ImageChooserPanel('header_image'),
        FieldPanel('text'),
        FieldPanel('featured_article'),
    ]

    subpage_types = ['website.BlogPost']
    parent_page_types = ['website.HomePage']

    def get_context(self, request):
        context = super().get_context(request)
        
        post_to_authors = {}

        authors = Teammate.objects.select_related('initial_photo').\
            prefetch_related('blogpost_set')

        for author in authors:
            for post in author.blogpost_set.select_related('cover_image').live():
                if post in post_to_authors:
                    post_to_authors[post].append(author)
                else:
                    post_to_authors[post] = [author]

        sorting_hat = {}
        for post in sorted(post_to_authors.keys(), key=operator.attrgetter('date'), reverse=True):
            sorting_hat[post] = post_to_authors[post]

        context['blog_posts'] = sorting_hat

        return context


class BlogPost(Page):
    cover_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    text = models.TextField()
    index_text = models.CharField(max_length=255)
    authors = ParentalManyToManyField(Teammate)
    categories = ParentalManyToManyField(Category)
    date = models.DateTimeField("Post date")

    content_panels = Page.content_panels + [
        ImageChooserPanel('cover_image'),
        FieldPanel('text'),
        FieldPanel('index_text'),
        FieldPanel('date'),
        FieldPanel('categories'),
        FieldPanel('authors')
    ]

    parent_page_types = ['website.BlogPostsPage']


class HackCast(Page):
    header_text = models.CharField(max_length=255, blank=True)
    header_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    subpage_types = []
    parent_page_types = ['website.HomePage']

    content_panels = Page.content_panels + [
        FieldPanel('header_text'),
        ImageChooserPanel('header_image')
    ]

    def get_context(self, request):
        context = super().get_context(request)
        context['episodes'] = HackCastEpisode.objects.order_by('-id')

        return context
