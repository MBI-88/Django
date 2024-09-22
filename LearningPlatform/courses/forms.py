from django import forms
from django.forms.models import inlineformset_factory
from .models import Course,Module

# Your forms here

ModuleFormSet = inlineformset_factory(Course,Module,fields=['title','description'],extra=2,can_delete=True)

#Nota: extra: permite 2 formularios mas vacios
#      can_delete: inserta un checkbutton en cada formulario para eliminar