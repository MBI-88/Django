# Packages
from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from django.urls import reverse_lazy
from .models import Post

# Class Feed

class LastPostsFeed(Feed):
    title = 'My blog'
    link = reverse_lazy('blog:post_list')
    description = 'New posts of my blog'
    
    def items(self):
        return Post.published.all()[:5]
    
    def item_title(self, item:object) -> str:
        return item.title
    
    def item_description(self, item:object) -> str:
        return truncatewords(item.body,30)