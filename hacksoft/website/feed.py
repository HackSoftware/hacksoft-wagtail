from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed, Rss201rev2Feed

from hacksoft.website.snippets import HackCastEpisode
from hacksoft.website.models import BlogPost


class FeedGenerator(Rss201rev2Feed):
    def add_root_elements(self, handler):
        super().add_root_elements(handler)

        if 'author_name' in self.feed:
            handler.addQuickElement('author_name', self.feed['author_name'])

        if 'author_email' in self.feed:
            handler.addQuickElement('author_email', self.feed['author_email'])

        if 'image' in self.feed:
            image = self.feed['image']

            handler.startElement('image', {})
            handler.addQuickElement('url', image['url'])
            handler.addQuickElement('title', image['title'])
            handler.addQuickElement('description', image['description'])
            handler.addQuickElement('link', image['link'])
            handler.endElement('image')

            handler.addQuickElement('itunes:image', '', {'href': image['url']})


class HackCastRssFeed(Feed):
    title = 'HackCast'
    link = '/hackcast/'
    description = 'HackCast is the official HackSoft podcast.'
    author_name = 'HackSoft'
    author_email = 'consulting@hacksoft.io'

    feed_type = FeedGenerator

    def items(self):
        return HackCastEpisode.objects.order_by('-id')

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.description

    def item_guid(self, item):
        return item.title

    def item_link(self, item):
        return item.mp3_url

    def item_enclosure_url(self, item):
        return item.mp3_url

    def item_enclosure_mime_type(self, item):
        return 'audio/mpeg'

    def item_enclosure_length(self, item):
        return item.duration

    def item_pubdate(self, item):
        return item.created_at

    def feed_extra_kwargs(self, item):
        return {
            'image': {
                'url': 'https://s3.eu-central-1.amazonaws.com/hackcast/hackcast_cover.png',
                'title': 'HackCast',
                'description': 'HackCast - The official HackSoft podcast.',
                'link': 'https://www.hacksoft.io/hackcast/'
            }
        }


class HackCastAtomFeed(HackCastRssFeed):
    feed_type = Atom1Feed
    subtitle = HackCastRssFeed.description


class BlogRssFeed(Feed):
    title = 'HackSoft Blog'
    link = '/blog/'
    description = 'HackSoft\'s official blog page'
    author_name = 'HackSoft'
    author_email = 'consulting@hacksoft.io'

    feed_type = FeedGenerator

    def items(self):
        return BlogPost.objects.order_by('-date')

    def item_title(self, item):
        return item.title

    def item_link(self, item):
        return item.full_url

    def item_description(self, item):
        return item.index_text


class BlogAtomFeed(BlogRssFeed):
    feed_type = Atom1Feed
    subtitle = BlogRssFeed.description
