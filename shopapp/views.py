from django.shortcuts import render
from django.views import View
from .forms import UserRegistrationForm
from .models import Product,Customer,Cart,OrderPlace
from django.contrib import messages
# def home(request):
#  return render(request, 'app/home.html')
class ProductView(View):
    def get(self,request):
        twear=Product.objects.filter(category='TW')
        bwear=Product.objects.filter(category='BW')
        mobiles=Product.objects.filter(category='M')
        return render(request, 'app/home.html',{'twear':twear,'bwear':bwear,'mobiles':mobiles})
# def product_detail(request):
#     return render(request, 'app/productdetail.html')

class ProductDetailView(View):
    def get(self,request,pk):
        product=Product.objects.get(pk=pk)
        return render(request, 'app/productdetail.html',{'product':product})

def add_to_cart(request):
 return render(request, 'app/addtocart.html')

def buy_now(request):
 return render(request, 'app/buynow.html')

def profile(request):
 return render(request, 'app/profile.html')

def address(request):
 return render(request, 'app/address.html')

def orders(request):
 return render(request, 'app/orders.html')

# def change_password(request):
#  return render(request, 'app/changepassword.html')

def mobile(request,data=None):
    if data==None:
        mobiles=Product.objects.filter(category='M')
    elif data=='Redmi' or data=='Samsung':
        mobiles=Product.objects.filter(category='M').filter(brand=data)
    elif data=='below':
        mobiles=Product.objects.filter(category='M').filter(discount_price__lt=4999)
    elif data=='above':
        mobiles=Product.objects.filter(category='M').filter(discount_price__gt=4999)
    return render(request, 'app/mobile.html',{'mobiles':mobiles})

# def login(request):
#  return render(request, 'app/login.html')

# def customerregistration(request):
#  return render(request, 'app/customerregistration.html')
class CustomerRegistrationView(View):
    def get(self,request):
        form=UserRegistrationForm()
        return render(request, 'app/customerregistration.html',{'form':form})

    def post(self,request):
        form=UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Congratulation !! Regisration successlully')
        return render(request, 'app/customerregistration.html',{'form':form})
def checkout(request):
 return render(request, 'app/checkout.html')