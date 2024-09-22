from django.shortcuts import render
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404
from .models import Order
from django.http import HttpResponse
from django.template.loader import get_template
from django.conf import settings
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders
import os



# Create your views here.

def order_create(request:str) -> render:
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount
            order.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,product=item['product'],
                    price=item['price'],quantity=item['quantity']
                )
            cart.clear()
            return render(request,'orders/order/created.html',{'order':order})
        
    else:
        form = OrderCreateForm()
    return render(request,'orders/order/create.html',{'cart':cart,'form':form})


@staff_member_required
def admin_order_detail(request:str,order_id:int) -> render:
    order = get_object_or_404(Order,id=order_id)
    return render(request,'admin/orders/order/detail.html',{'order':order})
        

# Convert html to pdf

@staff_member_required
def admin_order_pdf(request:str,order_id) -> HttpResponse:
    order = get_object_or_404(Order,id=order_id)
    uri = 'css/pdf.css'
    result = finders.find(uri)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=order_{}.pdf'.format(order.id)
    template = get_template('orders/order/pdf.html')
    
    if result:
        if not isinstance(result,(list,tuple)):
            result = [result]
        
        result = list(os.path.realpath(path) for path in result)
        path = result[0]

    html = template.render({'order':order})
    pisa_pdf = pisa.pisaDocument(
        html,dest=response,link_callback= lambda path: path
    )
    if pisa_pdf.err:
        return HttpResponse("We had some erros <pre>"+ html + "</pre>")

    return response

