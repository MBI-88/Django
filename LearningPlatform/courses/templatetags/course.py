from django import template 

register = template.Library()

@register.filter
def model_name(obj:object) -> object:
    try:
        return obj._meta.model_name
    except AttributeError:
        return None