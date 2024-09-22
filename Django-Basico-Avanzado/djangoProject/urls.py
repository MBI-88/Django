"""djangoProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import include
from django.conf import settings
from django.contrib import admin
from django.views.static import serve
from django.urls import path,re_path
from djangoProject.views import (fecha_actual, mi_csv, mi_imagen, mi_pdf,mipaginaHtml,horas_adelante,
                                 horas_adelante_M,atributos_meta,hola,fecha_M, vista_humanizada, vista_multiLanguage,vista_variada,
                                 peticion_get,peticion_post,show_librospage,libros_muestra,redirect_libros,
                                 vista1,scapeHtml,login_user,vista_logout,vista_login,vista_csrf_protect,selecLanguage,
                                 javascriptCatalog)
from biblioteca.views import *
from biblioteca.models import Libro,Editor
from biblioteca.feeds import UltimosLibrosAdjuntos, UltimosLibrosAtom, UltimosLibrosFedd, UltimosLibrosFeedComplex, UltimosLibrosFeedInfo
from contactos import views
from django.contrib.auth import views as auth_views # Vista generica para renderizar el formulario de loging
from django.contrib.auth.decorators import login_required
from django.contrib.sitemaps.views import sitemap,index
from biblioteca.sitemap import SitemapAutores, StaticViewSitemap
from django.contrib.sitemaps import GenericSitemap
from biblioteca.forms import registrar
from django.views.i18n import JavaScriptCatalog



# Para enganchar el sitemap generico
info_dic = {
    'queryset':Autor.objects.all(),
    'date_field': 'ultimo_acceso'
}
sitemaps = {
    'dynamic': GenericSitemap(info_dict=info_dic,priority=0.5,changefreq='always'),
    'static': StaticViewSitemap,
}




urlpatterns = [
    re_path(r'^admin/doc/',include('django.contrib.admindocs.urls')),
    path('admin/', admin.site.urls,name='Admin'),
    path("i18n/", include('django.conf.urls.i18n'), name="language"),
    path('jsi18n/',JavaScriptCatalog.as_view(),name='javascript-catalog'),
    path('hola/',hola,name='inicio'),
    path('fecha_actual/',fecha_actual),# Importacion básica
    re_path(r'^fecha/mas/(\d{1,2})/$', horas_adelante),
    path('mipaginaHtml',mipaginaHtml),# Variante mas corta de importacion
    path('fecha_M',fecha_M),
    re_path(r'horas_adelante/mas/(\d{1,2})/$', horas_adelante_M),
    path("atributos_meta", atributos_meta),
    re_path(r'^formulario-buscar/$', formulario_buscar),
    re_path(r'^buscar/$', buscar),
    re_path(r'^contactos/$', views.contactos),
    re_path(r'^redirect/$', views.redirect),# Variante mas economica de impotación / Solo se puede usar en un sitio
    re_path(r'^contActos', views.contActos),
    re_path(r'^contactos-personalizados/$', views.contactPersonal),
    re_path(r'^inicio/$', vista_indice, {'plantilla':'bienvenidos.html'}),
    re_path(r'^indice/$', vista_indice, {'plantilla':'indice.html'}),
    re_path(r'^lista_libros/$', lista_objetos,{'model':Libro}),
    re_path(r'^lista_editores/$', lista_objetos,{'model': Editor}),
    re_path(r'^indices/$', vista_variada,{'GET':peticion_get,'POST':peticion_post}),# uso de vista compartida
    re_path(r'^llenar/', include([ # Ejemplo de uso de include 
        re_path(r'^contactos-personalizados/$',views.contactPersonal),
        re_path(r'^contactos/$',views.contactos),
        re_path(r'^horas_adelante/mas/(\d{1,2})/$',horas_adelante_M),
    ])),
    re_path(r'^mostrar-libros/$', show_librospage),
    re_path(r'^libros-muestra', libros_muestra,name = 'libros-muestra'),
    re_path(r'^shorcuts/$', redirect_libros),
    re_path(r'^vista-plantilla/(?P<name>\w+)/$', vista1),
    re_path(r'^scapehtml/(\w+)/(\w+)/$', scapeHtml),
    re_path(r'^libroXautor/(\w+)/$', libroXautor),
    re_path(r'^vistaclase/', views.VistaSaludo.as_view()),
    re_path(r'^holamundo/', views.MiVista.as_view(), name = 'mi-vista'),
    re_path(r'^$', PaginaInicio.as_view(),name = 'Welcome'),
    re_path(r'^contador/(?P<pk>[0-9]+)/$', ContadorLibrosRedirectView.as_view(), name = 'contador-libros'),
    re_path(r'^detalles/(?P<pk>[0-9])/$', DetalleLibro.as_view(), name = 'detalle-libro'),
    re_path(r'^ir-a-django/$', RedirectView.as_view(url = 'http://djangoproject.com'), name = 'ir-a-django'),
    re_path(r'^acerca/', TemplateView.as_view(template_name = 'acerca_de.html')), # Paso directo de la url
    re_path(r'^editores/$', ListaEditores.as_view(), name = 'lista-editores'),
    re_path(r'^detalles/editor/(?P<pk>[0-9]+)/$', DetallesEditor.as_view(), name = 'detalle-editor'),
    re_path(r'^libros_recientes/$', LibrosRecientes.as_view(), name = 'libros-recientes'),
    re_path(r'^libros/([\D-]+)/$', ListaLibrosEditores.as_view(), name = 'libros-por-editores'),
    re_path(r'^autores/(?P<pk>[0-9]+)/$', VistaDetallesAutor.as_view(), name = 'detalles-autor'),
    re_path(r'^detalleEditores/(?P<pk>\w+)/$', DetalleEditores.as_view(), name = 'detalle_editores'),
    re_path(r'^contacts', views.MyFormFormView.as_view(), name = 'form-generic'),
    re_path(r'^autor/agregar/$', CrearAutor.as_view(), name = 'agregar-autor'),
    re_path(r'^autor/(?P<pk>\w+)/$', login_required(ActualizarAutor.as_view()), name = 'actualizar-autor'),
    re_path(r'^autor/(?P<pk>\w+)/borrar/$', BorrarAutor.as_view(), name = 'borrar-autor'),
    re_path(r'^accounts/login/$', auth_views.LoginView.as_view(), name = 'login-required'),
    re_path(r'^miImagen/$',mi_imagen,name = 'mostrar-imagen'),
    re_path(r'^csv/$', mi_csv, name = 'muestra-csv'),
    re_path(r'^pdf/$',mi_pdf, name ='muestra-pdf'),
    re_path(r'^pdfcomplejo/(?P<pk>\w+)/$',convertir_pdf,name='convert-pdf'),
    re_path(r'^feed/ultimoslibros.xml$', UltimosLibrosFedd(),name='feed-view'),
    re_path(r'^feed/ultimoslibrosinfo.xml$',UltimosLibrosFeedInfo(),name='feed-viewInfo'),
    re_path(r'^atom/ultimoslibrosatom.xml$', UltimosLibrosAtom(),name='feed-viewAtom'),
    re_path(r'^feed/adjuntos.xml$',UltimosLibrosAdjuntos(),name='feed-viewAdjuntos'),
    re_path(r'^complex/(?P<px>\w+)/rss.xml$',UltimosLibrosFeedComplex(),name='feed-viewComplex'),
    re_path(r'^sitemapautores.xml$',sitemap,{'sitemaps':{'sitemaps':SitemapAutores}},name='sitemap-autores'),
    re_path(r'^sitemapgenerico.xml$',sitemap,{'sitemaps':{'blog':GenericSitemap(info_dict=info_dic,priority=0.5,changefreq='always')}}
            ,name='sitemap-generic'),
    re_path(r'sitemapsStatic.xml$',sitemap,{'sitemaps':{'sitempas':StaticViewSitemap}},name='sitemap-static'),
    re_path(r'^sitemapindex.xml$',index,{'sitemaps':sitemaps},name='django.contrib.sitemaps.views.index'),
    re_path(r'^sitemapindex-(?P<section>.+).xml$',sitemap,{'sitemaps':sitemaps},name='django.contrib.sitemaps.views.sitemap'),
    re_path(r'^loginUser/$',login_user,name='login-user'),
    re_path(r'^accounts/profile/$',vista_login,name='login-session'),
    re_path(r'^accounts/logout/$',vista_logout,name='logout-session'),
    re_path(r'^registrar/$',registrar,name='user-register'),
    re_path(r'^csrf_protect/',vista_csrf_protect,name='vista-csrf-protected'),
    re_path(r'^humanizada/',vista_humanizada,name='vista-humanizada'),
    path('internacional/',vista_multiLanguage,name='vista-internacional'),
    path('chooseLang/',selecLanguage,name='select-language'),
    path('usojs/',javascriptCatalog,name='vista-js'),
    
    
]

if (settings.DEBUG):
    #urlpatterns += [url(r'^debuginfo/$',debug)] pertenece a djangoProject
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$',serve,{'document_root':settings.MEDIA_ROOT})
    ]
