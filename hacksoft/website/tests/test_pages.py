from wagtail.tests.utils import WagtailPageTests
from ..models import (HomePage, BlogPostsPage, BlogPost,
                      ContactsPage, PortfolioPage, OurTeamPage,
                      TechnologiesWeUsePage, HowWeWorkPage)


class PageTests(WagtailPageTests):

    def test_can_create_contacts_page_from_homepage(self):
        self.assertCanCreateAt(HomePage, ContactsPage)

    def test_can_create_portfolio_page_from_homepage(self):
        self.assertCanCreateAt(HomePage, PortfolioPage)

    def test_can_create_ourteam_page_from_homepage(self):
        self.assertCanCreateAt(HomePage, OurTeamPage)

    def test_can_create_technologies_page_from_homepage(self):
        self.assertCanCreateAt(HomePage, TechnologiesWeUsePage)

    def test_can_create_howwework_page_from_homepage(self):
        self.assertCanCreateAt(HomePage, HowWeWorkPage)

    def test_can_create_blogposts_page_from_homepage(self):
        self.assertCanCreateAt(HomePage, BlogPostsPage)

    def test_can_create_blogposts_from_blogposts_page(self):
        self.assertCanCreateAt(BlogPostsPage, BlogPost)
