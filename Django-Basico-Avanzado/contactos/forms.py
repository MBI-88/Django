# Modulos
from django import forms

# Classes

class FormularioContactos(forms.Form):
    asunto = forms.CharField(min_length=3,max_length=100)
    email = forms.EmailField(required=False,label="Direccion")
    mensaje = forms.CharField(widget=forms.Textarea)

    def clean_mensaje(self) -> str:
        mensaje = self.cleaned_data['mensaje']
        num_palabras = len(mensaje.split())
        if (num_palabras < 4):
            raise forms.ValidationError("¡Se require mínimo 4 palabras")
        return mensaje
    
    # Metodo para el uso de vistas genericas
    def send_email(self) -> None:
        # Enviar datos como en seccion anterior 
        print("Email sent")
        



    

