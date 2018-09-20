from django.conf import urls
from django.conf.urls import url

from . import views


app_name = 'website'
urlpatterns = [
    url(r'^(?P<slug>[-\w]+)/', views.BlogPostView.as_view(), name='blog_page'),
]
