from django.urls import path
from . import views

urlpatterns = [
    path('', views.store, name="store"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('update_item/', views.updateItem, name="update_item"),
    path('process_order/', views.processOrder, name="process_order"),
    path('product/<int:id>', views.productView, name="product_view"),
    path('contact/', views.contact, name="contact"),
    path('promotions/', views.promotions, name="promotions"),
    path('our_stores/', views.map, name="our_stores")
]
