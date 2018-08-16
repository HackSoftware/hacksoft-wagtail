from django.contrib.syndication.views import Feed

from hacksoft.website.snippets import HackCastEpisode


class HackCastFeed(Feed):
    title = 'HackCast'
    link = '/hackcast/'
    description = 'HackCast is the official HackSoft podcast.'

    def items(self):
        return HackCastEpisode.objects.order_by('-id')

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.description

    def item_link(self, item):
        return item.mp3_url
