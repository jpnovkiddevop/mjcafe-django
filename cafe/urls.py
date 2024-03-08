from django.urls import path
from . import views
from cart import views as cartViews

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('search/', views.search, name='search'),
    path('update_user/', views.Update_user, name='update-user'),
    path('update_password/', views.update_user_password, name='update-password'),
    path('add_menu_item/', views.add_menu_item, name='add-menu'),
    path('menuitem/<slug:slug>/', views.menu_item, name='menu-item'),
    path('category/<slug:slug>/', views.category, name='category'),
    path('user_details/<slug:slug>/', views.user_details, name='user_details'),
    # for ajax request to add or remove items in cart
    path('cart_items/', cartViews.cart_items, name="cart_items"),
]
