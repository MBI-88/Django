# Packages
from distutils.errors import LibError
from django.contrib.syndication.views import Feed
from django.utils import feedgenerator
from biblioteca.models import Editor, Libro
from django.urls import reverse
from django.shortcuts import get_object_or_404

# Classes
# Feed sencillo
class UltimosLibrosFedd(Feed):
    feed_type = feedgenerator.Rss201rev2Feed
    title = "Feed libros publicados"
    link = "/ultimos-libros/"
    description = "Ultimos libros publicados en la biblioteca digital"
    title_template = 'feeds/ultimoslibros_title.html'
    #description_template = 'feeds/ultimoslibros_description.html'
    
    def items(self) -> object:
        return Libro.objects.order_by("-fecha_publicacion")[:2]
    
    def item_title(self, item:object) -> str:
        return item.titulo
    
    #def item_description(self, item:object) -> str:
     #   return item.descripcion
    
    def item_link(self, item:object) -> reverse:
        return reverse('detalle-libro',args=[item.pk])
    
    def item_enclosure_url(self, item:object) -> str:
        address = str(item.portada.url).split('/',3)[3]
        return address
    
    def item_enclosure_length(self, item:object) -> int:
        return item.portada.size


item_enclosure_mime_type = "image/jpeg"


# Pasando informacion extra
class UltimosLibrosFeedInfo(Feed):
    title = 'Mis libros'
    link = "/ultimos-libros/"
    description_template = 'feeds/ultimoslibros_description.html'
    
    def items(self) -> object:
        return Libro.objects.order_by('-fecha_publicacion')[:2]
    
    def get_context_data(self, **kwargs) -> dict:
        context = super(UltimosLibrosFeedInfo,self).get_context_data(**kwargs)
        context['foo'] = 'bar'
        return context
    
    def item_link(self, item:object) -> reverse: # indispensable su existencia
        return reverse('detalle-libro',args=[item.pk])



# Feeds con adjuntos
class UltimosLibrosAdjuntos(Feed):
    title = 'Ultimas portadas de libros'
    link = '/feeds/ejemplo-con-adjuntos/'
    
    def items(self) -> object:
        return Libro.objects.all()[:2]
    
    def item_enclosure_url(self,item:object) -> str:
        address = str(item.portada.url).split('/',3)[3]
        return address
    
    def item_enclosure_length(self, item:object) -> int:
        return item.portada.size
    
    def item_link(self, item:object) -> reverse:
        return reverse('detalle-libro',args=[item.pk])


# Publicando varios Feed (usando como parte el primer feed de Ultimos libros)
class UltimosLibrosAtom(UltimosLibrosFedd):
    feed_type = feedgenerator.Atom1Feed
    subtitle = UltimosLibrosFedd.description
    

# Feed complejos
class UltimosLibrosFeedComplex(Feed):
    description = 'feeds/ultimoslibros_description.html'
    
    def get_object(self, request, px:int) -> object:
        self.px = px
        return get_object_or_404(Editor, pk=px)
    
    def title(self,obj:object) -> str:
        return "Nombre %s" % obj.nombre
    
    def description(self,obj:object) -> str:
        return "Pais de nacimiento %s" % obj.pais
    
    def link(self,obj:object) -> str:
        return "Url: %s" % obj.website
    
    def items(self,obj:object) -> object:
        return  obj.libro_set.all()
    
    def item_link(self, item:object) -> reverse:
        return reverse('detalle-editor',args=[self.px])
    
    
