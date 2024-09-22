from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ImageCreateForm
from django.shortcuts import get_object_or_404
from .models import Image
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from common.decorators import ajax_required
from django.http import HttpResponse
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from actions.utils import create_action

# Create your views here.

@login_required
def image_create(request:str) -> render:
    if request.method == 'POST':
        form = ImageCreateForm(data=request.POST)
        if form.is_valid():
            new_item = form.save(commit=False)
            new_item.user = request.user
            new_item.save()
            create_action(request.user,'bookmarked image',new_item)
            messages.success(request,'Image added successfully')
            return redirect(new_item.get_absolute_url())
    else:
        form = ImageCreateForm(data=request.GET)
    
    return render(request,'images/image/create.html',{'section':'images','form':form})

def image_detail(request:str,id:int,slug:str) -> render:
    image = get_object_or_404(Image,id=id,slug=slug)
    return render(request,'images/image/detail.html',{'section':'images','image':image})


@ajax_required
@login_required
@require_POST
def image_like(request:str) -> JsonResponse:
    image_id = request.POST.get('id')
    action = request.POST.get('action')
    if image_id and action:
        try:
            image = Image.objects.get(id=image_id)
            if action == 'like':
                image.users_like.add(request.user)
                create_action(request.user,'likes',image)
            else:
                image.users_like.remove(request.user) # remove/add/clear son metodos del campo de relacion manytomany
            
            return JsonResponse({'status':'ok'})
        except:
            pass 
    return JsonResponse({'status':'error'})


@login_required
def image_list(request:str) -> render:
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    images = Image.objects.all()
    paginator = Paginator(images,9)
    page = request.GET.get('page')
    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        images = paginator.page(1)
    except EmptyPage:
        if is_ajax:
            return HttpResponse('')
        images = paginator.page(paginator.num_pages)
    
    if is_ajax:
        return render(request,'images/image/list_ajax.html',{'section':'images','images':images})
    
    return render(request,'images/image/list.html',{'section':'images','images':images})
    


            