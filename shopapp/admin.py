from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Customer,Cart,OrderPlace,Product
# Register your models here.

class CustomerModelAdmin(admin.ModelAdmin):
    list_display=['id','user','name','locality','city','zipcode','state']

admin.site.register(Customer,CustomerModelAdmin)

class ProductModelAdmin(admin.ModelAdmin):
    list_display=['id','title','selling_price','discount_price','description','brand','category','product_image']

admin.site.register(Product,ProductModelAdmin)

class CartModelAdmin(admin.ModelAdmin):
    list_display=['id','user','product','quantity']

admin.site.register(Cart,CartModelAdmin)


@admin.register(OrderPlace)
class OrderPlaceModelAdmin(admin.ModelAdmin):
    list_display=['id','user','customer','product','quantity','order_date','status']


# def product_info(self,obj):
#     link=reverse("admin:shopapp_customer_change",args=[obj.product.pk])
#     return format_html('<a href="{}">{}</a>',link,obj.customer.title)


# def customer_info(self,obj):
#     link=reverse("admin:app_customer_change",args=[obj.customer.pk])
#     return format_html('<a href="{}">{}</a>',link,obj.customer.name)

