# Formulario de inscripcion para usuarios en biblioteca

# Packages
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Form
def registrar(request:str) -> render:
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect('/libros_recientes/')
    else:
        form = UserCreationForm()
    
    return render(request,'registro.html',{'form':form})