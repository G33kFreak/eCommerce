import json
from .models import *

def cookieCart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}

    items = []
    order = {'get_cart_total': 0, 'get_cart_items': 0}
    cartItems = order['get_cart_items']

    for i in cart:
        cartItems += cart[i]['count']
        product  = Product.objects.get(id=i)
        total = (product.price * cart[i]['count'])
        order['get_cart_total'] += total
        order['get_cart_items'] += cart[i]['count']

        item = {
            'product': {
                'id':product.id,
                'name':product.name,
                'price':product.price,
                'imageURL':product.imageURL
            },
            'count':cart[i]['count'],
            'get_total':total,
        }
        items.append(item)
    return {'cartItems':cartItems, 'order':order, 'items':items}


def cartData(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']

    return {'cartItems':cartItems, 'order':order, 'items':items}