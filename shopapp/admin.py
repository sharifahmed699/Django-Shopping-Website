from django.contrib import admin
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

class OrderPlaceModelAdmin(admin.ModelAdmin):
    list_display=['id','user','customer','product','quantity','order_date','status']

admin.site.register(OrderPlace,OrderPlaceModelAdmin)