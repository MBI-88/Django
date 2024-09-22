from django import forms
from .models import Comment

# Forms Class

class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False,widget=forms.Textarea)

# Se usa ModelForm porque la creacion del formulario es dinamica
# Para excluir campos usar exclude en lugar de fields
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment 
        fields = ('name','email','body')


class SearchForm(forms.Form):
    query = forms.CharField(max_length=50)
