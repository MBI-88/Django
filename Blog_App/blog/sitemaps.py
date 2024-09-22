# Packages
from django.contrib.sitemaps import Sitemap
import priority
from .models import Post


# Class Sitemap

class PostSitemaps(Sitemap):
    changefreq = 'weekly'
    priority = 0.9
    
    def items(self):
        return Post.published.all()
    
    def lastmod(self,obj:object) -> object:
        return obj.updated

