import json
from .models import *


def cookieCart(request):
    try:
        # json.loads is django's way of doing json.parse(). Data sent to client browser is normally stringified, so need to parse or json.loads it so we can work with it 
        cart = json.loads(request.COOKIES['cart'])

    except:
        cart = {}
        print("cart is ", cart)

        

    items = []
    order = {'get_cart_total':0,'get_cart_items':0,'shipping':False}
    cartitems = order['get_cart_items']

    for i in cart:
        try:
            cartitems += cart[i]['quantity']
            product = Product.objects.get(id = i)
            total = (product.price * cart[i]['quantity'])

            order['get_cart_total'] += total
            order['get_cart_items'] += cart[i]['quantity']
            
            
            
            item = {
                'product':{
                    "id":product.id,
                    'name':product.name,
                    "price":product.price,
                    "imageURL":product.imageURL
                },

                "quantity":cart[i]['quantity'],

                "get_total":total
            } 

            if (product.digital == False):
                order['shipping'] = True

            items.append(item)

        except:
            pass
    return {"items":items,"order":order,"cartitems":cartitems}

    
def cartData(request):
        
    if request.user.is_authenticated:
        print(request.user)
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer = customer,complete = False)
        items = order.orderitem_set.all()

        # _set.all allows us to do reverse search/query on the model
        #  _set.all allows is used on foreign key values for reverse query 
        #  _set.all is used to (reverse) query for that specific object

        cartitems = order.get_cart_items
        
    else:
        items = []

    # Line below has to be there otherwise you'd get a local variable referenced before assignment, error . Because variable such as order will try to get value globally if line isnt there

        order = {'get_cart_total':0,'get_cart_items':0}


        
        cookieData = cookieCart(request)
        cartitems = cookieData['cartitems']
        order = cookieData['order']
        items = cookieData['items']

    return {"items":items,"order":order,"cartitems":cartitems}

def guestOrder(request,data):
    cookieData = cookieCart(request)
    items = cookieData['items']

    name = data['userformdata']['name']
    email = data['userformdata']['email']

    customer, created = Customer.objects.get_or_create(
            email = email
        )

    customer.name = name
    customer.save()

    order = Order.objects.create(
            customer = customer,
            complete = False
        )
    
    for item in items:
        product = Product.objects.get(id = item['product']['id'])

        orderItem = OrderItem.objects.create(
                product = product,
                order = order,
                quantity = item['quantity'] if item['quantity']>0 else -1*item['quantity'],
            ) 

    return customer, order

