from django.shortcuts import render,redirect

from customer.forms import RegistrationForm,LoginForm
from django.views.generic import View
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login
from store.models import Products,Carts,Orders,Offers

class SignUpView(View):

    def get(self,request,*args,**kwrags):
        form=RegistrationForm()
        return render(request,"signup.html",{"form":form})
    def post(self,request,*args,**kw):
        form=RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("signup")
        else:
            return render(request,"signup.html",{"form":form})



class SignInView(View):
    def get(self,request,*args,**kw):
        form=LoginForm()
        return render(request,"login.html",{"form":form})
    def post(self,request,*args,**kw):
        form=LoginForm(request.POST)

        if form.is_valid():
            uname=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            usr=authenticate(request,username=uname,password=pwd)
            print(usr)
            if usr:
                login(request,usr)
                return redirect("home")
            else:
                return render(request,"login.html",{"form":form})


class IndexView(View):
    def get(self,request,*args,**kw):
        qs=Products.objects.all()
        return render(request,"index.html",{"products":qs})

class ProductDetailView(View):

    def get(self,request,*args,**kwargs):
        id=kwargs.get("id")
        qs=Products.objects.get(id=id)
        return render(request,"product-detail.html",{"product":qs})

class AddToCartView(View):

    def post(self,request,*args,**kwargs):
        print(request.POST.get("qty"))
        qty=int(request.POST.get("qty"))
        user=request.user
        id=kwargs.get("id")
        product=Products.objects.get(id=id)
        Carts.objects.create(product=product,user=user,qty=qty)
        return redirect("home")

class CartListView(View):

    def get(self,request,*args,**kwargs):
        qs=Carts.objects.filter(user=request.user,status="in-cart")
        return render(request,"cart-list.html",{"carts":qs})


class CartRemoveView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("id")
        Carts.objects.filter(id=id).update(status="cancelled")
        return redirect("home")


class MakeOrderView(View):

    def get(self,request,*args,**kwargs):
        id=kwargs.get("id")
        qs=Carts.objects.get(id=id)
        return render(request,"checkout.html",{"cart":qs})
    def post(self,request,*args,**kwargs):
       user=request.user
       address=request.POST.get("address")
       id=kwargs.get("id")
       cart=Carts.objects.get(id=id)
       product=cart.product
       Orders.objects.create(product=product,
       user=user,
       address=address)
       cart.status="order-placed"
       cart.save()
       return redirect("home")

class MyoredrsView(View):
    def get(self,request,*args,**kwargs):
        qs=Orders.objects.filter(user=request.user).exclude(status="cancelled")
        return render(request,"order-list.html",{"orders":qs})
        


class OrderCancellView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("id")
        Orders.objects.filter(id=id).update(status="cancelled")
        return redirect("my-orders")

class DiscountProductsView(View):

    def get(self,request,*args,**kwargs):
        qs=Offers.objects.all()
        return render(request,"offer-products.html",{"offers":qs})