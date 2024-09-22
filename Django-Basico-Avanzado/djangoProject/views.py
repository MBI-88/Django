__author__ = 'MBI'
__doc__ = """
Script para desorrollo de vista en Django.
Nota: Una vista es solo una funcion python (solo una).
"""
#==== Packages ====#
import csv
from doctest import REPORT_UDIFF
from reportlab.pdfgen import canvas
from django import template
from django.http import Http404, HttpResponseRedirect, HttpResponse, FileResponse
import datetime as dt
from django.template import Context
from django.template.loader import render_to_string,get_template
from django.shortcuts import render
from django.urls import reverse
from django.template import RequestContext,Template
from django.contrib.auth import login,logout,authenticate
from django.views.decorators.csrf import csrf_protect


#==== Function ====#

HTML = """
<!DOCTYPE html>
<html lang="es">
<head>
<meta http­equiv="content­type" content="text/html; charset=utf­8">
<meta name="robots" content="NONE,NOARCHIVE">
<title>Hola mundo</title>
<style type="text/css">
html * { padding:0; margin:0; }
body * { padding:10px 20px; }
body * * { padding:0; }
body { font:small sans­serif; }
body>div { border­bottom:1px solid #ddd; }
h1 { font­weight:normal; }
#summary { background: #e0ebff; }
</style>
</head>
<body>
<div id="summary">
<h1>¡Hola Mundo!</h1>
</div>
</body></html>
"""

def hola(request:str) -> HttpResponse:
    return HttpResponse(HTML)

def fecha_actual(request:str) -> HttpResponse:
    now = dt.datetime.now()
    #tem = get_template('fecha_actual.html')
    #html = render_to_string('fecha_actual.html',context={'fecha_actual':now})
    html = render(request,template_name='fecha_actual.html',context={'fecha_actual':now})
    #html = tem.render(context={'fecha_actual':now},request=request)
    return html

def horas_adelante(request:str,offset:str) -> HttpResponse:
    try:
        offset = int(offset)
    except ValueError:
        raise Http404()
    
    hora = dt.datetime.now() + dt.timedelta(hours=offset)
    html = "<html><body><h1>En {} hora(s), seran:</h1> <h3>{}</h3></body></html>".format(offset,hora)
    return HttpResponse(html)

def mipaginaHtml(request:str) -> HttpResponse:
    html = render(request,'mipagina.html',context={
        'titulo':"Probando etiquta include",
        'seccion_actual': 'Etiqueta nav'
    })
    return html

def fecha_M(request:str) -> HttpResponse:
    now = dt.datetime.now()
    html = render(request,'fecha_M.html',context={
        'fecha_actual':now
    })
    return html

def horas_adelante_M(request:str,offset:str) -> HttpResponse:
    try:
        offset = int(offset)
    except ValueError:
        raise Http404()
    hora = dt.datetime.now() + dt.timedelta(hours=offset)
    return render(request,'horas_adelante_M.html',context={'hora_siguiente':hora,
    'horas':offset})

def atributos_meta(request:str) -> HttpResponse:
    valor = request.META.items()
    html:list[str] = []
    for k,v in valor:
        html.append((k,v))
    return render(request,"RequestMeta.html",context={"titulo":"Data user","userdata":html})

"""
Uso para caso de extraer variables de la url

def vista_dividida(request,*args,**kwargs) -> render:
    vista_get = kwargs.pop('GET',None)
    vista_post = kwargs.pop('POST',None)
    if (request.method == 'GET' and vista_get is not None):
        return vista_get(request,*args,**kwargs)
    elif (request.method == 'POST' and vista_post is not None):
        return vista_post(request,*args,**kwargs)
    raise Http404

def vista_get(request,*args,**kwargs) -> render:
    assert request.method == 'GET'
    return render(request,'peticionGet.html',{})

def vista_post(request,*args,**kwargs) -> render:
    assert request.method == 'POST'
    return render(request,'peticionPost.html',{})

"""
# No se extrae variables de la url
def vista_variada(request,GET=None,POST=None) -> render:
    if (request.method == 'GET' and GET is not None):
        return GET(request)
    elif (request.method == 'POST' and POST is not None):
        return POST(request)
    raise Http404

def peticion_get(request) -> render:
    assert request.method == 'GET'
    return render(request,'peticionGet.html')

def peticion_post(request) -> render:
    assert request.method == 'POST'
    return render(request,'peticionPost.html')

def libros_muestra(request) -> render:
    libros:list[str] = ["Libro 1","Libro 2","Libro 3"]
    return render(request,'libros-muestra.html',{'muestra':libros})

def show_librospage(request) -> render:
    return render(request,'showlibros.html')

def redirect_libros(request) -> HttpResponseRedirect:
    return HttpResponseRedirect(reverse("libros-muestra",args=None))

# Uso de procesadores de contexto

def custom_proc(request) -> dict:
    "Un procesador de contexto que provee 'aplicacion','usuario' y 'direccion_ip'"
    return {
        'aplicacion':'Mi app',
        'usuario':request.user,
        'direccion_ip':request.META['REMOTE_ADDR']
    }

def vista1(request,name=None) -> HttpResponse:
   template = Template(template_string="""
    <div style="margin: 10px 20px;background: -moz-linear-gradient();">
        <hgroup style="color: blueviolet;">
            <h1 style="margin-bottom: 15px;">{{mensaje}}</h1>
            <h2>{{aplicacion}}</h2>
            <h2>{{usuario}}</h2>
            <h2>{{direccion_ip}}</h2>
        </hgroup>
    </div>
   """)
   contexto = RequestContext(request,processors=[custom_proc])
   contexto.push({'mensaje':name})
   return HttpResponse(template.render(contexto))

# Probando el scape html
def scapeHtml(request,name=None,cadena=None) -> render:
    "Funcion para probar el escapdo en html" # Usar para documentar las vistas
    return render(request,'ScapeHtml.html',{'name':name,'cadena':cadena})


# Mostrando contenido no HTML

# Mostrando imagen
def mi_imagen(request:str) -> HttpResponse:
    return FileResponse(open("media/HelloWorld.jpg",'rb'))

# Mostrando csv
def mi_csv(request:str) -> HttpResponse:
    response = HttpResponse(content_type = 'text/csv')
    response['Content-Disposition'] = 'attachment; filename=cualquiera.csv'
    
    write_csv = csv.writer(response)
    write_csv.writerow(['Año','Pasajeros problematicos en aerolinea'])
    for (year, num) in zip(range(1995, 2006),[146,184,235,200,226,251,299,273,281,304,203]):
        write_csv.writerow([year, num])
    
    return response


# Generando PDF 
def mi_pdf(request:str) -> HttpResponse:
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=hello.pdf'
    pdf = canvas.Canvas(response)
    pdf.roundRect(0,750,694,120,20,stroke=0,fill=1)
    pdf.setFillColorRGB(0,1,1)
    pdf.setFont('Times-Bold',28)
    pdf.drawString(50,800,'Bienvenido a Django')
    pdf.setFont('Times-Bold',12)
    pdf.drawString(250,780,'Hola mundo')
    pdf.setFont('Times-Bold',150)
    pdf.drawString(70,400,'Django')
    pdf.showPage()
    pdf.save()
    return response

# Funcion de login para usar login y logout

def login_user(request:str) -> render:
    return render(request,'loginUser.html')

# Autenticacion de usario en la session de django
def vista_login(request:str) -> HttpResponseRedirect:
    username = request.POST['username']
    password = request.POST['password']
    usr = authenticate(request,username=username,password=password)
    if (usr is not None):
        login(request,usr)
        return HttpResponseRedirect('/inicio/')
    return HttpResponse('<h1>Autentication Failed </h1>')
    

def vista_logout(request:str) -> HttpResponseRedirect:
    logout(request)
    return render(request,'registration/logout.html')

@csrf_protect
def vista_csrf_protect(request:str) -> render: # Solo para la prueba de csrf manual (el uso de response ya lo incluye si 
    # se usa la capa de procesamiento CSRFViewMiddleware) esto es lo mismo que usar el csrf_token en los tamplate y tener
    # activa la capa anterior
    context = {
        'name':'prueba de csrf'
    }
    return render(request,'csrf_template.html',context)

# Uso de los filtros del modulo humanize
def vista_humanizada(request:str) -> render:
    context = {
        'numberFloat': 4500,
        'numberMillon': 1000000,
        'timeNow':dt.datetime.now(),
        'ordinals': 10,
    }
    return render(request,'tample_humanize.html',context=context)

# Vistas para probar la internacionalizacion
def vista_multiLanguage(request:str) -> render:
    return render(request,'International.html')

# Seleccionar un idioma
def selecLanguage(request:str) -> render:
    return render(request,'LanguageForm.html')

# Uso del catalogo JS
def javascriptCatalog(request:str) -> render:
    return render(request,'JavaScriptCatalog.html')