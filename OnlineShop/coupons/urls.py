from django.urls import path
from . import views

# Your urls here
app_name = 'coupons'

urlpatterns = [
    path('apply/',views.coupon_apply,name='apply')
]