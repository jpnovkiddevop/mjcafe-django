
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.http import HttpResponse
from cafe.models import MenuItem, Order, Customer
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
import requests
import base64
import datetime

from mjcafe.siri import my_consumer_key, my_business_short_code, my_consumer_secret, my_pass_key

PRICE = 0.00

def cart_summary(request):
    global PRICE
    cart = request.session.get('cart', [])
    cart_quantity = len(cart)
    # Reset price for cart summary
    PRICE = 0.00
    for cart_item in cart:
        PRICE += float(cart_item.get('price')) * int(cart_item['quantity'])
    context = {
        'cart_items': cart,
        'total_quantity': cart_quantity,
        'price': PRICE
               }
    return render(request, 'cart/cart_summary.html', context)


def cart_add(request, slug):
    item = get_object_or_404(MenuItem, slug=slug)
    cart = request.session.get('cart', [])
    cart.append({
        'slug': item.slug,
        'name': item.name,
        'price': str(item.selling_price) if item.selling_price else str(item.price),
        'quantity': 1,
    })
    request.session['cart'] = cart
    return redirect('home')


def cart_items(request):
    global PRICE
    cart_quantity = len(request.session.get('cart', []))
    cart_items = request.session.get('cart', [])
    PRICE = 0.00  # Reset price for cart items
    for cart_item in cart_items:
        PRICE += float(cart_item.get('price')) * int(cart_item['quantity'])
    return JsonResponse({'cart_quantity': cart_quantity, 'price': PRICE})


def cart_delete(request):
    global PRICE
    if request.method == 'POST':
        slug = request.POST.get('item_slug')
        if 'cart' in request.session:
            cart_items = request.session.get('cart', [])
            updated_cart_items = []

            # Flag to indicate if the item was found and deleted
            item_found = False

            for item in cart_items:
                if item.get('slug') == slug:
                    item_found = True
                    PRICE -=  float(item.get('price')) * int(item.get('quantity'))
                else:
                    updated_cart_items.append(item)

            if item_found:
                request.session['cart'] = updated_cart_items
                cart_quantity = len(updated_cart_items)
                return JsonResponse({'success': True, 'cart_quantity': cart_quantity, 'price':PRICE},
                                    status=200)
            else:
                return JsonResponse({'success': False, 'error': 'Item not found in cart'}, status=404)

    return JsonResponse({'success': False, 'error': 'Method not allowed'}, status=405)



def calculate_order_amount(request):
    # Retrieve the cart items from the session
    cart_items = request.session.get('cart', [])
    
    total_amount = 0.0

    # Calculate the total amount by summing up the prices of all items in the cart
    for cart_item in cart_items:
        item_slug = cart_item.get('slug')
        quantity = int(cart_item.get('quantity', 0))
        
        # Retrieve the MenuItem object based on the slug
        menu_item = MenuItem.objects.filter(slug=item_slug).first()
        
        if menu_item:
            if menu_item.selling_price:
                item_price = menu_item.selling_price
            else:
                item_price = menu_item.price
            
            total_amount += float(item_price) * quantity

    # You can return the total amount in a JSON response or render a template with the amount
    return render(request, 'cart/amount_calculation.html', {'total_amount': total_amount})

#order processing and integration with daraja api will be handled to completion on a later date 
def place_order(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            
        # Process the order and cart items
            # Assuming you have 'amount' and 'phone_number' available from the request or other sources
            amount = calculate_order_amount(request) 
            phone = request.POST.get('phone') 

            # Initiate payment
            response = initiate_payment(amount, phone)
            if response:
                # Handle the payment initiation response
                print(response)
                return redirect('order-confirmation')
            else:
                # Handle errors or provide feedback to the user
                messages.success(request, ('failed to  process your order'))
                return redirect('cart-summary')
    else:
        messages.success(request, ('please login to place an order'))
        return redirect('login')

def order_confirmation(request):

    messages.success(request, ('your order was placed successfuly!.Thank you for choosing mj kitchen'))
    return render(request, 'cart/order_confirmation.html', {})


# Function to initiate payment requests using Daraja API
def initiate_payment(amount, phone):
    access_token = get_access_token()
    if access_token:
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json',
        }
        payload = {
            'BusinessShortCode': settings.SAFARICOM_SHORTCODE,
            'Password': generate_password(),
            'Timestamp': generate_timestamp(),
            'TransactionType': 'CustomerPayBillOnline',
            'Amount': amount,
            'PartyA': phone,
            'PartyB': settings.SAFARICOM_SHORTCODE,
            'PhoneNumber': phone,
            'CallBackURL': settings.SAFARICOM_CALLBACK_URL,
            'AccountReference': 'MJkitchen',
            'TransactionDesc': 'Payment for services',
        }
        response = requests.post(
            settings.SAFARICOM_PAYMENT_URL, json=payload, headers=headers)
        return response.json()
    return None


def get_access_token():
    consumer_key = my_consumer_key
    consumer_secret = my_consumer_secret
    api_url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'

    # Send a request to get the access token
    response = requests.get(api_url, auth=(consumer_key, consumer_secret))

    # Parse the response and extract the access token
    if response.status_code == 200:
        access_token = response.json().get('access_token')
        return access_token
    else:
        # Handle errors or return None
        return None


def generate_password():
    pass_key = my_pass_key
    business_short_code = my_business_short_code
    timestamp = generate_timestamp()

    # Concatenate the business short code, pass key, and timestamp
    data_to_encode = business_short_code + pass_key + timestamp

    # Encode the data in base64
    encoded_data = base64.b64encode(
        data_to_encode.encode('utf-8')).decode('utf-8')

    return encoded_data

def generate_timestamp():
    # Generate current timestamp in the required format
    timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    return timestamp
