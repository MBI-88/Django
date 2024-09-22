# Packages
from django.contrib.sitemaps import Sitemap
from biblioteca.models import Autor
from django.urls import reverse

# Classes

class SitemapAutores(Sitemap):
    changefreq = 'monthly'
    priority = 0.5
    
    def items(self) -> object:
        return Autor.objects.all()
    
    def lastmod(self,items:object) -> str:
        return items.ultimo_acceso

# Solucion para indexar vistas estaticas
class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'daily'
    
    def items(self) -> list:
        return ['libros-muestra','mi-vista','Welcome','lista-editores','muestra-csv','muestra-pdf']
    
    def location(self,item:str) -> reverse:
        return reverse(item)