from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.http import HttpResponse
from .models import *
from django.core.mail import send_mail
import json
import datetime

from .utils import cookieCart, cartData, guestOrder


def store(request):

    data = cartData(request)
    cartItems = data['cartItems']
    activeState = {'store':'active', 'promo':'', 'stores':'', 'contact':''}

    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems, 'state': activeState}
    return render(request, 'store/store.html', context)

def promotions(request):
    data = cartData(request)
    cartItems = data['cartItems']
    activeState = {'store':'', 'promo':'active', 'stores':'', 'contact':''}
    promos = Product.objects.filter(promotion__gt=0)

    context = {'cartItems': cartItems, 'state': activeState, 'promos':promos}
    return render(request, 'store/promotions.html', context)

def map(request):
    data = cartData(request)
    cartItems = data['cartItems']
    activeState = {'store':'', 'promo':'', 'stores':'active', 'contact':''}
    mapAccessToken = 'pk.eyJ1IjoiZzMza2ZyZWFrIiwiYSI6ImNrYmdvbDYzbjE3cXoyenM3Z3pwd2MzOXYifQ.IKHnxZDwoq7Ny0InK1985A'
    address = Contact.objects.get(pk=1).address

    context = {'cartItems': cartItems, 'state': activeState, 'mapbox_access_token': mapAccessToken, 'address':address}

    return render(request, 'store/map.html', context)

def contact(request):
    data = cartData(request)
    cartItems = data['cartItems']
    activeState = {'store':'', 'promo':'', 'stores':'', 'contact':'active'}
    contact = Contact.objects.get(pk=1)

    context = {'cartItems': cartItems, 'state': activeState, 'contact':contact}
    return render(request, 'store/contact.html', context)



def cart(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/cart.html', context)


def main(request):
    context = {}
    return render(request, 'store/main.html', context)


def checkout(request):

    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/checkout.html', context)

def productView(request, id):
    data = cartData(request)
    cartItems = data['cartItems']
    product = get_object_or_404(Product, id=id)
    
    context = {'product':product, 'cartItems':cartItems}

    return render(request, 'store/product_view.html', context)



def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(
        customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(
        order=order, product=product)

    if action == 'add':
        orderItem.count = (orderItem.count + 1)
    elif action == 'remove':
        orderItem.count = (orderItem.count - 1)

    orderItem.save()

    if orderItem.count == 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
    else:
        customer, order = guestOrder(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True
    order.save()

    ShippingInfo.objects.create(
        customer=customer,
        order=order,
        address=data['shipping']['address'],
        city=data['shipping']['city'],
        code=data['shipping']['code'],
    )

    emailMessage = 'Dear, {}!\nThank you for your order in our VapeShop!\nYour order numer is {}.\nAll the best,\nVapeShop team'.format(customer.name, order.transaction_id)

    send_mail('Order successfully placed', emailMessage, '', [customer.email])

    return JsonResponse('Payment complete', safe=False)
