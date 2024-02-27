import email
from http.cookies import CookieError
from math import prod
from pickle import FALSE
from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from .models import *
import json
import datetime
from .utils import cookieCart,cartData,guestOrder
from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.models import User
from .models import User
from .forms import MyUserCreationForm
from django.contrib import messages
from django.db.models import Q

# Create your views here. 

def store(request): 

    category = Category.objects.all()
    q = request.GET.get('q') if request.GET.get('q') != None else ""

    products = Product.objects.filter(Q(category__name__icontains=q))
                                        
    
    cartdata = cartData(request)
    items = cartdata['items']
    order = cartdata['order']
    cartitems = cartdata['cartitems']



    
    context = {"products":products,"cartitems":cartitems,"category":category}
    return render(request,"store/shop.html",context)

def cart(request):
   

    products = Product.objects.all()
    cartdata = cartData(request)
    items = cartdata['items']
    order = cartdata['order']
    cartitems = cartdata['cartitems']


   
    context = {"items":items,"order":order,"cartitems":cartitems}
    return render(request,"store/cart.html",context)


def checkout(request):
    

    cartdata = cartData(request)
    items = cartdata['items']
    order = cartdata['order']
    cartitems = cartdata['cartitems']

        
    context = {"items":items,"order":order,"cartitems":cartitems}
    return render(request,"store/checkout.html",context)
 


def updatedItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print("productid :" , productId)
    print("action :" , action)


    customer = request.user.customer
    product = Product.objects.get(id = productId)
    order, created = Order.objects.get_or_create(customer = customer,complete = False)

    orderItem, created = OrderItem.objects.get_or_create(order = order, product = product)
    
    if action == 'add':
        orderItem.quantity = orderItem.quantity + 1

    elif action == 'remove':
        orderItem.quantity = orderItem.quantity - 1

    elif action == 'clear':
        orderItem.quantity = 0

    orderItem.save()

    if orderItem.quantity <=0:
        orderItem.delete()


    
    return JsonResponse("Item was added just now",safe=False)


def processOrder(request):

    # json.loads is django's way of doing json.parse(). Data sent to client browser is normally stringified, so need to parse or json.loads it so we can work with it 
    data = json.loads(request.body)
    transactionid = datetime.datetime.now().timestamp()
    userInfo = data['userformdata']
    shippinginfo = data['shippinginfo']

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer = customer, complete = False)

    else:

        customer, order = guestOrder(request,data)


    order.transaction_id = transactionid
    total = float(data['userformdata']['total'])
       
    if total == float(order.get_cart_total):
        order.complete = True

    order.save()   

    if order.shipping == True:
            ShippingAddress.objects.create(
                customer = customer,
                order = order,
                address = shippinginfo['address'],
                city = shippinginfo['city'],
                state = shippinginfo['state'],
                zipcode = shippinginfo['zipcode']
            )


    print("request: ", request.COOKIES)
     
    return JsonResponse(" SUCCESS : payment was submitted",safe=False)


    

def thankyou(request):


    return render(request,"store/thankyou.html") 


def services(request):
    products = Product.objects.all()
    cartdata = cartData(request)
    cartitems = cartdata['cartitems']
    context = {'products':products,"cartitems":cartitems}
    return render(request,"store/services.html",context) 


def about(request):
    cartdata = cartData(request)
    cartitems = cartdata['cartitems']
    context = {'cartitems':cartitems}
    return render(request,"store/about.html",context) 

def contact(request):

    cartdata = cartData(request)
    cartitems = cartdata['cartitems']
    context = {'cartitems':cartitems}


    return render(request,"store/contact.html",context) 

def login_user(request):

    page = "login"
    cartdata = cartData(request)
    cartitems = cartdata['cartitems']

    

    if request.user.is_authenticated:
        return redirect('store')

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request,username = email, password = password)

        if user is not None:
            login(request,user)
            return redirect('store')
            
        else:
            print("whats wrong")


    context = {"page":page,"cartitems":cartitems}
    return render(request,'store/index.html',context)

def createUser(request):

    # form = MyUserCreationForm()



    # if request.method == "POST":
    #         form = MyUserCreationForm(request.POST)

    #         if form.is_valid():
            
    #             user = form.save(commit = False)
    #             user.username = user.username.lower()
    #             user.save()
    #             login(request,user)
    #             return redirect('store')
    #         else:
    #             messages.error(request,'some error in registration')
    
    # context = {"form" : form}

    cartdata = cartData(request)
    cartitems = cartdata['cartitems']
    form = MyUserCreationForm()

    if request.method == "POST":
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit = False)
            user.username = user.username.lower()
            user.save()
            customer = Customer.objects.create(user = user, name = user.username, email = user.email)
            login(request,user)
            return redirect("store")
        else:
            messages.error(request,"Error in registration")
    context = {"form":form,"cartitems":cartitems}
        

    return render(request,"store/index.html",context)


def logoutUser(request):
    logout(request)
    return redirect('store') 

# def clearData(request):

#     data = json.loads()
#     data




