# Script to keep tags

# Modules
from django import template
from datetime import datetime
import re
from biblioteca.models import Libro



# Classes
class NodoFechaActual(template.Node):
    def __init__(self,formato_cadena) -> None:
        self.formato_cadena = str(formato_cadena)
    
    def render(self, context: template.Context) -> str:
        ahora = datetime.now()
        return ahora.strftime(self.formato_cadena)

# Creando una variable en el contexto. Crea problemas de sobre escritura si se vuelve a utilizar
class NodoFechaActual2(template.Node):
    def __init__(self,formato_cadena) -> None:
        self.formato_cadena = str(formato_cadena)
    
    def render(self, context: template.Context) -> str:
        ahora = datetime.now()
        context['fecha_actual'] = ahora.strftime(self.formato_cadena)
        return ''

# Resolviendo el problema anterior
class NodoFechaActual3(template.Node):
    def __init__(self,formato_cadena,var_nombre) -> None:
        self.formato_cadena = str(formato_cadena)
        self.var_nombre = var_nombre
    
    def render(self, context: template.Context) -> str:
        ahora = datetime.now()
        context[self.var_nombre] = ahora.strftime(self.formato_cadena)
        return ''

class CommentNode(template.Node):
    def render(self, context: template.Context) -> str:
        return ''

class UpperNode(template.Node):
    def __init__(self,nodelist:str) -> None:
        self.nodellist = nodelist
    
    def render(self, context: template.Context) -> str:
        output = self.nodellist.render(context)
        return output.upper()

# Function
register = template.Library()

@register.filter(name='cortar')
def cortar(valor:str,arg:str) -> str:
    """Remueve todos los argumentos que concuerdan
       con la cadena data"""
    return valor.replace(arg,'')

@register.filter
def minusculas(valor) -> str:
    return valor.lower()

@register.tag(name='fecha_actual')
def fecha_actual(parser,token:str) -> str:
    try:
        tag_nombre,formato_cadena = token.split_contents()
    except ValueError:
        msg = "%r la etiqueta requiere un simple argumento" % token.split_contents()[0]
        raise template.TemplateSyntaxError(msg)
    return NodoFechaActual(formato_cadena[1:-1])

@register.tag
def fecha_actual2(parser,token:str) -> str:
    try:
        tag_nombre,formato_cadena = token.split_contents()
    except ValueError:
        msg = "%r la etiqueta requiere un simple argumento" % token.split_contents()[0]
        raise template.TemplateSyntaxError(msg)
    return NodoFechaActual2(formato_cadena[1:-1])


# Funciones que forman parte de la solucion
@register.tag(name='traer_fecha_actual')
def traer_fecha_actual(parser,token) -> str:
    try:
        tag_nombre,arg = token.contents.split(None,1)
    except ValueError:
        msg = "%r la etiqueta requiere un simple argumento" % token.split_contents()[0]
        raise template.TemplateSyntaxError(msg)
    
    m = re.search(r'(.*?) as (\w+)',arg)

    if m:
        fmt, var_nombre = m.groups()
        
    else:
        msg = '%r Argumentos no validos para la etiqueta' % tag_nombre
        raise template.TemplateSyntaxError(msg)
    
    if not (fmt[0] == fmt[-1] and fmt[0] in ('"',"'")): # pregunta si existen comillas simples o dobles
        msg = "%r Los argumentos deben de ir entre comillas" % tag_nombre
        raise template.TemplateSyntaxError(msg)
    
    return NodoFechaActual3(fmt[1:-1],var_nombre)

@register.tag(name='do_comment')
def do_comment(parser,token:str) -> str:
    nodelist = parser.parse(('endcomment',))
    parser.delete_first_token()
    return CommentNode()

@register.tag
def upper(parser,token:str) -> str:
    nodelist = parser.parse(('endupper',))
    parser.delete_first_token()
    return UpperNode(nodelist)

# Uso de simple_tag
@register.simple_tag
def mi_prueba(token) -> str:
    bienvenido = "Welcome"+" "+token+" !"
    return bienvenido

@register.simple_tag
def fecha_nueva(token) -> str:
    return datetime.now().strftime(token)

# uso plantillas inclusivas
@register.inclusion_tag('inclusiontag.html',takes_context=True)
def inclusiontag(context) -> dict:
    libros = Libro.objects.all()
    return {'libros':libros,
            'link':'http://localhost:8000/admin',
            'title':context['title']
            }

