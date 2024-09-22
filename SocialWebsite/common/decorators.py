from django.http import HttpResponseBadRequest

def ajax_required(f) -> object:
    def wrap(request:str,*args,**kwargs) -> object:
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        if not is_ajax:
            return HttpResponseBadRequest()
        return f(request,*args,**kwargs)
    
    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__
    return wrap