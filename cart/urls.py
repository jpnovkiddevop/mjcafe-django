from django.urls import path
from . import views

urlpatterns = [
    path('', views.cart_summary, 
         name='cart-summary'),
    path('add_to_cart/<slug:slug>/', 
         views.cart_add, name='cart-add'),
    #path('remove_from_cart/<slug:slug>/', 
     #    views.remove_from_cart, name='remove-from-cart'),
    #path('delete_from_cart/',
        #views.cart_delete, name='cart-delete'),
    #path('update_cart/', views.cart_update, 
     #    name='cart-update'),
    path('cart_delete/', views.cart_delete, name='cart_delete'),
    path('place_order/', views.place_order, 
         name='place-order'),
    path('order_confirmation/<str:order_number>/',views.order_confirmation,
         name='order-confirmation'),
    path('iniate_payment/', views.initiate_payment,
         name='initiate_payment'),
]