from django.shortcuts import render,redirect
from django.views import View
from .forms import UserRegistrationForm,CustomerProfileForm
from .models import Product,Customer,Cart,OrderPlace
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
# def home(request):
#  return render(request, 'app/home.html')
class ProductView(View):
    def get(self,request):
        twear=Product.objects.filter(category='TW')
        bwear=Product.objects.filter(category='BW')
        mobiles=Product.objects.filter(category='M')
        count=0
        if request.user.is_authenticated:
            count=len(Cart.objects.filter(user=request.user))
        return render(request, 'app/home.html',{'twear':twear,'bwear':bwear,'mobiles':mobiles,'count':count})
# def product_detail(request):
#     return render(request, 'app/productdetail.html')

class ProductDetailView(View):
    def get(self,request,pk):
        product=Product.objects.get(pk=pk)
        item_in_cart=False
        count=0
        if request.user.is_authenticated:
            count=len(Cart.objects.filter(user=request.user))
            item_in_cart=Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
        return render(request, 'app/productdetail.html',{'product':product,'item_in_cart':item_in_cart,'count':count})

@login_required
def add_to_cart(request):
    user=request.user
    product_id=request.GET.get('prd_id')
    product=Product.objects.get(id=product_id)
    Cart(user=user,product=product).save()
    return redirect('/cart')

@login_required
def show_cart(request):
    if request.user.is_authenticated:
        user=request.user
        count=0
        count=len(Cart.objects.filter(user=request.user))
        cart=Cart.objects.filter(user=user)
        amount=0.0
        shipping_amount = 50.0
        total_amount=0.0
        cart_product=[p for p in Cart.objects.all() if p.user == user]
        if cart_product:
            for p in cart_product:
                tamount=(p.quantity*p.product.discount_price)
                amount+=tamount
                total_amount=amount+shipping_amount
            return render(request, 'app/addtocart.html',{'cart':cart,'total_amount':total_amount,'amount':amount,'shipping_amount':shipping_amount,'count':count})
        else:
            return render(request,'app/emptycart.html')

def plus_cart(request):
    if request.method=='GET':
        prod_id=request.GET['prd_id']
        cart=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        cart.quantity+=1
        cart.save()

        amount=0.0
        shipping_amount = 50.0
        total_amount=0.0
        cart_product=[p for p in Cart.objects.all() if p.user == request.user]
        if cart_product:
            for p in cart_product:
                tamount=(p.quantity*p.product.discount_price)
                amount+=tamount
              
            data={
                'quantity':cart.quantity,
                'amount':amount,
                'totalamount':amount + shipping_amount
            }
            return JsonResponse(data)
           

def minus_cart(request):
    if request.method=='GET':
        prod_id=request.GET['prd_id']
        cart=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        cart.quantity-=1
        cart.save()
        amount=0.0
        shipping_amount = 50.0
        total_amount=0.0
        cart_product=[p for p in Cart.objects.all() if p.user == request.user]
        if cart_product:
            for p in cart_product:
                tamount=(p.quantity*p.product.discount_price)
                amount+=tamount
                
            data={
                'quantity':cart.quantity,
                'amount':amount,
                'totalamount':amount + shipping_amount
            }
            return JsonResponse(data)


def remove_cart(request):
    if request.method=='GET':
        prod_id=request.GET['prd_id']
        # cart=get_object_or_404(Cart, Q(product=prod_id) & Q(user=request.user))
        cart=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        # cart=Cart.objects.filter(Q(product=prod_id) & Q(user=request.user))
        cart.delete()
        amount=0.0
        shipping_amount = 50.0
        total_amount=0.0
        cart_product=[p for p in Cart.objects.all() if p.user == request.user]
        if cart_product:
            for p in cart_product:
                tamount=(p.quantity*p.product.discount_price)
                amount+=tamount
                
            data={
                'amount':amount,
                'totalamount':amount + shipping_amount
            }
            return JsonResponse(data)
        else:
            return render(request,'app/emptycart.html')


def buy_now(request):
 return render(request, 'app/buynow.html')

# def profile(request):
#  return render(request, 'app/profile.html')

@method_decorator(login_required,name='dispatch')
class ProfileView(View):
    def get(self,request):
        count=0
        if request.user.is_authenticated:
            count=len(Cart.objects.filter(user=request.user))
        form=CustomerProfileForm()
        return render(request, 'app/profile.html',{'form':form,'active':'btn-primary','count':count})

    def post(self,request):
        form=CustomerProfileForm(request.POST)
        if form.is_valid():
            user=request.user
            name=form.cleaned_data['name']
            locality=form.cleaned_data['locality']
            city=form.cleaned_data['city']
            state=form.cleaned_data['state']
            zipcode=form.cleaned_data['zipcode']
            reg=Customer(user=user,name=name,locality=locality,city=city,state=state,zipcode=zipcode)
            reg.save()
            messages.success(request,'Congratulation !! Profile Update successlully')
        return render(request, 'app/profile.html',{'form':form,'active':'btn-primary'})

@login_required
def address(request):
    count=0
    if request.user.is_authenticated:
        count=len(Cart.objects.filter(user=request.user))
    customer=Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html',{'customer':customer,'active':'btn-primary','count':count})

@login_required
def orders(request):
    count=0
    if request.user.is_authenticated:
            count=len(Cart.objects.filter(user=request.user))
    op=OrderPlace.objects.filter(user=request.user)
    return render(request, 'app/orders.html',{'op':op,'count':count})

# def change_password(request):
#  return render(request, 'app/changepassword.html')

def mobile(request,data=None):
    count=0
    if request.user.is_authenticated:
        count=len(Cart.objects.filter(user=request.user))
    if data==None:
        mobiles=Product.objects.filter(category='M')
    elif data=='Redmi' or data=='Samsung':
        mobiles=Product.objects.filter(category='M').filter(brand=data)
    elif data=='below':
        mobiles=Product.objects.filter(category='M').filter(discount_price__lt=4999)
    elif data=='above':
        mobiles=Product.objects.filter(category='M').filter(discount_price__gt=4999)
    return render(request, 'app/mobile.html',{'mobiles':mobiles,'count':count})

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

@login_required
def checkout(request):
    user=request.user
    count=0
    if request.user.is_authenticated:
        count=len(Cart.objects.filter(user=user))
    add=Customer.objects.filter(user=user)
    cart_item=Cart.objects.filter(user=user)
    amount=0.0
    shipping_amount = 50.0
    total_amount=0.0
    cart_product=[p for p in Cart.objects.all() if p.user == user]
    if cart_product:
        for p in cart_product:
            tamount=(p.quantity*p.product.discount_price)
            amount+=tamount
            total_amount=amount+shipping_amount
        totalamount= amount + shipping_amount
    return render(request, 'app/checkout.html',{'add':add,'cart_item':cart_item,'totalamount':totalamount,'count':count})


@login_required
def payment_done(request):
    user=request.user
    cust_id=request.GET.get('custid')
    customer=Customer.objects.get(id=cust_id)
    cart=Cart.objects.filter(user=user)
    for c in cart:
        OrderPlace(user=user,customer=customer,product=c.product,quantity=c.quantity).save()
        c.delete()
    return redirect("orders")

