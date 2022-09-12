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

# Create your views here. 

def store(request):
    products = Product.objects.all()
    
    cartdata = cartData(request)
    items = cartdata['items']
    order = cartdata['order']
    cartitems = cartdata['cartitems']
        
       
        

    context = {"products":products,"cartitems":cartitems}
    return render(request,"store/shop.html",context)

def cart(request):
    # customers = Customer.objects.all()
   
    # orders = Order.objects.all()
    # orderitems = OrderItem.objects.all()
    # orderitemsNo = orderitems.count()
    
    # totalcost = 0
    # for i in orderitems:
    #     totalcost = totalcost + (i.product.price * i.quantity)
     # context = {"customers":customers,"products":products,"orders":orders,"orderitems":orderitems,"orderitemsNo":orderitemsNo,"totalcost":totalcost}

    products = Product.objects.all()
    cartdata = cartData(request)
    items = cartdata['items']
    order = cartdata['order']
    cartitems = cartdata['cartitems']

        
         # _set.all allows us to do reverse search/query on the model
        #  _set.all allows is used on foreign key values for reverse query 
        #  _set.all is used to (reverse) query for that specific object
    
        
    
    

   
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
        # total = float(data['userformdata']['total'])
       
        # if total == float(order.get_cart_total):
        #     order.complete = True

        # order.save()    

        

       
    
        

        # 
        # Below line is wrong becuase it says, if shipping address exists, then ammend the address, when i should actually just create a new address for the customer
        # shippingadd, created = ShippingAddress.objects.get_or_create(customer = customer)

        

        # shippingadd.order = Order.objects.get(customer = customer, complete = False)
        # shippingadd.address = shippinginfo['address']
        # shippingadd.city = shippinginfo['city']
        # shippingadd.state = shippinginfo['state']
        # shippingadd.save()
        # print(request.body)

    # print(creditds)

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

        # customer = "Anonymous"
        # order, created = Order.objects.get_or_create(customer = 'customer', complete = False)
        # total = float(data['userformdata']['total'])
       
        # if total == float(order.get_cart_total):
        #     order.complete = True

        # order.save()    
        # order.transaction_id = transaction 

        # shippinginfo = data['shippinginfo']

        # if order.shipping == True:
        #     ShippingAddress.objects.create(
        #         customer = customer,
        #         order = order,
        #         address = shippinginfo['address'],
        #         city = shippinginfo['city'],
        #         state = shippinginfo['state'],
        #         zipcode = shippinginfo['zipcode']
        #     )


    print("request: ", request.COOKIES)
     
     


     

    return JsonResponse(" SUCCESS : payment was submitted",safe=False)

def thankyou(request):

    return render(request,"store/thankyou.html") 


def services(request):

    return render(request,"store/services.html") 


