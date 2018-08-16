from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed

from hacksoft.website.snippets import HackCastEpisode


class HackCastRssFeed(Feed):
    title = 'HackCast'
    link = '/hackcast/'
    description = 'HackCast is the official HackSoft podcast.'
    author_name = 'HackSoft'
    author_email = 'consulting@hacksoft.io'

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


class HackCastAtomFeed(HackCastRssFeed):
    feed_type = Atom1Feed
    subtitle = HackCastRssFeed.description
