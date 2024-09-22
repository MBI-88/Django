from django.shortcuts import render, get_object_or_404
from django.http import Http404, HttpResponse, HttpResponseRedirect
from biblioteca.models import Libro, Editor, Autor
from django.views.generic.base import TemplateView, RedirectView
from django.views.generic import ListView, DetailView
from django.utils import timezone
from django.views.generic.detail import SingleObjectMixin
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from io import BytesIO
from reportlab.pdfgen import canvas





# Create your views here.

def formulario_buscar(request:str) -> HttpResponse:
    return render(request,'formulario_buscar.html')

def buscar(request:str) -> HttpResponse:
    errors:list[str] = [] 
    if 'q' in request.GET:
       q = request.GET['q']
       if not q:
           errors.append('Por favor introdusca un termino de búsqueda.')
       elif len(q) > 20:
            errors.append('Por favor introdusca un termino de búsqueda menor a 20 caracteres.')
       else:
            libros = Libro.objects.filter(titulo = q)
            return render(request,'resultados.html',{'libros':libros,'query':q})
    return render(request,'formulario_buscar.html',{'errors':errors})

def vista_indice(request:str,plantilla:str) -> render: # uso del 3er argumento para usar 2 o mas vistas con la misma función
    libros = Libro.objects.all()
    return render(request,plantilla,{'libros':libros})

def lista_objetos(request:str,model:object) -> render:
    lista_objetos = model.objects.all()
    plantilla = '%s_lista.html'% model.__name__.lower()
    return render(request,plantilla,{'lista_objetos':lista_objetos})

def libroXautor(request:str,name:str,title:str='Admin') -> dict:
    return render(request,'display_books.html',{'name':name,'title':title })

# Vistas basadas en clases genricas base
class PaginaInicio(TemplateView):
    template_name = "Welcome.html"
    
    def get_context_data(self, **kwargs) -> dict:
        context = super(PaginaInicio,self).get_context_data(**kwargs)
        context['ultimos_libros'] = Libro.objects.all()
        return context

class ContadorLibrosRedirectView(RedirectView):
    permanet = False
    query_string = True
    pattern_name = 'detalle-libro'

    def get_redirect_url(self, *args, **kwargs) -> HttpResponse:
        libro = get_object_or_404(Libro, pk = kwargs['pk']) # Devuelve un elemeto del obejto libro, pk funciona como indice de busqueda
        return super(ContadorLibrosRedirectView, self).get_redirect_url(*args, **kwargs)



# Vistas genericas de objetos
class DetalleLibro(DetailView):
    template_name = 'detalle_libro.html'
    model = Libro

class ListaEditores(ListView):
    template_name = 'editor_list.html'
    model = Editor
    # context_object_name = 'lista_editores' para cambiar el nombre de la variable del contexto

class DetallesEditor(DetailView):
    template_name = 'detalle_editor.html'
    model = Editor

    """ Extendiendo el contexto para listar todos los libros y los datos de editores
    def get_context_data(self, **kwargs) -> dict:
        context = super(DetallesEditor, self).get_context_data(**kwargs)
        context['lita_libros'] = Libro.objects.all()
        return context
    """

class LibrosRecientes(ListView):
    template_name = 'libros_recientes.html'
    queryset = Libro.objects.order_by('-fecha_publicacion')
    context_object_name = 'libros_recientes'

    def head(self, *agrs, **kwargs) -> HttpResponse: # Soporte para Apis
        ultimos_libros = self.get_queryset().latest('fecha_publicacion')
        response = HttpResponse('')
        response['modificados'] = ultimos_libros.fecha_publicacion.strftime(
            '%a, %d %b %Y %H:%M:%S GMT'
        )
        # Nota el metodo no funciona porque no se establecieron fechas como requerido
        return response

# Filtrado dinamico
class ListaLibrosEditores(ListView):
    template_name = 'libros_por_editores.html'
    context_object_name = 'librosXeditores'
    
    def get_queryset(self) -> list: 
        self.editor = get_object_or_404(Editor, nombre = self.args[0])
        return Libro.objects.filter(editor = self.editor)


class VistaDetallesAutor(DetailView):
    queryset = Autor.objects.all()
    template_name = 'detalles_autor.html'
    context_object_name = 'detallesAutor'

    def get_object(self) -> object:
        objeto = super(VistaDetallesAutor, self).get_object()
        objeto.ultimo_acceso = timezone.now()
        objeto.save()
        return objeto

# Uso de mixin
class DetalleEditores(SingleObjectMixin, ListView):
    paginate_by = 1
    template_name = 'detalleEditores.html'

    def get(self,request, *args, **kwargs) -> HttpResponse:
        self.object = self.get_object(queryset = Editor.objects.all())
        return super(DetalleEditores, self).get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs) -> dict[str, object]:
        context = super(DetalleEditores, self).get_context_data(**kwargs)
        context['editor'] = self.object
        return context
        
    def get_queryset(self) -> list[object]:
        return self.object.libro_set.all()


# Seccion perteneciente a forms.py (Para vistas de formularios)
# Uso de CRUD
class CrearAutor(CreateView):
    model = Autor
    fields = ['nombre','apellidos','email']
    template_name = "autor_form.html"

    @method_decorator(login_required)
    def dispatch(self, request:HttpResponse, *args, **kwargs) -> HttpResponse:
        return super().dispatch(request, *args, **kwargs)

    
class ActualizarAutor(UpdateView):
    model = Autor
    fields = ['nombre','apellidos','email']
    template_name = "autor_form.html"

    
class BorrarAutor(DeleteView):
    model = Autor
    success_url = reverse_lazy('detalles-autor')
    pattern_name = '/redirect/'
   

# Creando pdf conplejos
def convertir_pdf(request:str, pk:int) -> HttpResponse:
    try:
        libro = Libro.objects.get(id=pk)
    except ValueError:
        raise Http404()
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="archivo.pdf"'
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer)
    pdf.roundRect(0, 750,694,120,20,stroke=0,fill=1)
    pdf.setFont('Times-Bold',32)
    pdf.setFillColorRGB(1,1,1)
    pdf.drawString(100,800,str(libro.titulo))
    address = str(libro.portada.url).split('/',maxsplit=3)[3]
    pdf.drawImage(str(address),100,100,width=400,height=600)
    pdf.showPage()
    pdf.save()
    pdf_complex = buffer.getvalue()
    buffer.close()
    response.write(pdf_complex)
    return response




