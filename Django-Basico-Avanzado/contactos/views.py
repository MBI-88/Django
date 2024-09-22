from django.shortcuts import render
from django.core.mail import send_mail
from django.http import  HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from contactos.forms import FormularioContactos
from django.views.generic import View
from django.views.generic import FormView



# Create your views here.

def contactos(request) -> render:
    errors:list[str] = []
    if request.method == 'POST':
        if not request.POST.get('asunto',''):
            errors.append('Por favor introdusca un asunto')
        
        elif not request.POST.get('mensaje',''):
            errors.append('Por favor introdusca un mensaje')
        
        elif request.POST.get('email') and '@' not in request.POST['email']:
            errors.append('Por favor introdusca una direccion de email valida')
        
        elif  not errors:
            send_mail(request.POST["asunto"],request.POST["mensaje"],request.POST.get("email","noreply@example.com"),["stieowenr@example.com"])
            return HttpResponseRedirect('/redirect/')
        
    return render(request,"formulario_contactos.html",{"errors":errors,
                                                        "asunto":request.POST.get("asunto",""),
                                                        "mensaje":request.POST.get("mensaje",""),
                                                        "email":request.POST.get("email","")})


def redirect(request) -> render:
    return render(request,"gracias.html")

# Rescribiendo la vista contacto con el uso de class form

def contActos(request) -> render:
    if request.method == "POST":
        form:object = FormularioContactos(request.POST)
        print(form,"  ",type(form))
        if form.is_valid():
            cd:dict = form.cleaned_data # obteniendo los datos procesados sin errores
            send_mail(cd['asunto'],cd['mensaje'],cd.get('email','noreply@example.com'),['siteowner@example.com']
            )
            return HttpResponseRedirect('/redirect/')
    else:
        form = FormularioContactos(initial={'asunto':'¡Asunto importante!'})
    return render(request,'formulario_contactosForm.html',{'form':form})

def contactPersonal(request) -> render:
    if request.method == "POST":
        form = FormularioContactos(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            send_mail(cd['asunto'],cd['mensaje'],cd.get('email','noreply@example.com'),['siteowner@example.com'])
            return HttpResponseRedirect('/redirect/')
    else:
        form = FormularioContactos(initial={'asunto':'¡Asunto importante!','mensaje':'¡Escriba aqui!'})
    return render(request,'formulario_personalizado.html',{'form':form})

# Uso de vistas basadas clases
class VistaSaludo(View):
    #saludo = "Buenos dias"

    def get(self,request) -> render:
        return render(request,'vistaClase.html')

class MiVista(View):
    def get(self,request, *args, **kwargs) -> HttpResponse:
        return HttpResponse('Hola Mundo')


# Vista basada en clase generica manipulando formularios
# Ejemplo con View
class MyFormView(View):
    form_class = FormularioContactos
    initial = {'key':'value'} 
    template_name = 'formulario_contactosForm.html'

    def get(self, request, *agrs, **kwargs) -> render:
        form = self.form_class(initial = self.initial)
        return render(request, self.template_name, {'form':form})

    def post(self, request, *args, **kwargs) -> render:
        form = self.form_class(request.POST)
        if form.is_valid():
           cleaned:dict =  form.cleaned_data
           return HttpResponseRedirect('/redirect/')
        return render(request, self.template_name, {'form':form})

# Ejemplo con FormView
class MyFormFormView(FormView):
    form_class = FormularioContactos
    template_name = 'formulario_contactosForm.html'
    success_url = '/redirect/'

    def form_valid(self, form: object) -> HttpResponse:
        form.send_email()
        return super().form_valid(form)
    
    def form_invalid(self, form:object) -> HttpResponse:
        print("Falló")
        return super().form_invalid(form)