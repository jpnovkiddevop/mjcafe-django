from django.shortcuts import render, redirect, HttpResponseRedirect
from .models import MenuItem, Category
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .forms import SignUpForm, UpdateUserForm, ChangeUserPassword, MenuForm
from .models import Customer
#from django.db.models import Q

# Create your views here.


def search(request):
    if request.method == 'POST':
        searched = request.POST['searched']
        searched_results = MenuItem.objects.filter(name__icontains=searched)
        if searched:
            return render(request, 'cafe/search.html', {'searched': searched_results, 'query': searched})
        else:
            return render(request, 'cafe/search.html', {})
    else:
        return render(request, 'cafe/search.html', {})


def user_details(request, slug):
    if request.user.is_authenticated:
        current_user = Customer.objects.get(slug=slug)
        return render(request, 'cafe/user_details.html', {'current_user': current_user})
    else:
        messages.success(request, ('login to view your details'))
        return redirect('login')


def category(request, slug):
    try:
        category = Category.objects.get(slug=slug)
        menu_items = MenuItem.objects.filter(category=category)
        return render(request, 'cafe/category.html', {'category': category, 'menuitems': menu_items})
    except:
        messages.success(request, ('category doesnt exist..'))
        return redirect('home')


def add_menu_item(request):
    submitted = False
    if request.method == 'POST':
        form = MenuForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, ('food item added successfully'))
            return HttpResponseRedirect('/add_menu_item?submmited=True')

    else:
        form = MenuForm()
        if submitted in request.GET:
            submitted = True
        return render(request, 'cafe/add_menu.html', {"form": form})


def menu_item(request, slug):
    cart = request.session.get('cart', [])
    menu_item = MenuItem.objects.get(slug=slug)
    context = {
        'cart': cart,
        'menuitem': menu_item
    }
    return render(request, 'cafe/menu_item.html', context)


def home(request):
    menu_items = MenuItem.objects.all()
    cart = request.session.get('cart', [])
    total_quantity = len(cart)
    context = {
        'menuitems': menu_items,
        'total_quantity': total_quantity
    }
    return render(request, 'cafe/home.html', context)


def about(request):
    return render(request, 'cafe/about.html', {})


def login_user(request):
    if request.method == "POST":  # If the form has been submitted...
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:  # The password verified
            login(request, user)
            messages.success(
                request, (f'logged in !.. Karibu {username} to Mj jikoni the home of quality snacks'))
            return redirect('home')
        else:
            messages.success(
                request, ('error occurred while logging in..try again'))
            return redirect('login')
    return render(request, 'cafe/login.html', {})


def logout_user(request):
    logout(request)
    messages.success(
        request, ('logged out successfully..thank you for choosing Mj kitchen'))
    return redirect('login')


def register_user(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            # Create a Customer instance linked to the registered user
            customer = Customer.objects.create(
                user=user,
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                email=form.cleaned_data['email'],
            )
            messages.success(
                request, (f'registration account for {username} successfull'))
            login(request, user)
            return redirect('home')
        else:
            messages.success(
                request, ('Registration failed, please try again..'))
            return redirect('register')
    else:
        return render(request, 'cafe/register.html', {'form': form})


@login_required
def Update_user(request):
    current_user = request.user
    try:
        customer = current_user.customer
    except Customer.DoesNotExist:
        # Handle the case where Customer doesn't exist for the user
        customer = None

    form = UpdateUserForm(request.POST or None, instance=current_user)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            # Update Customer details
            if customer:
                customer.first_name = form.cleaned_data['first_name']
                customer.last_name = form.cleaned_data['last_name']
                customer.email = form.cleaned_data['email']
                customer.save()

            messages.success(
                request, f'Hey {current_user.username}, your Profile has been updated !!')
            return redirect('home')
        else:
            messages.error(
                request, 'There was an error in the form. Please correct it.')

    return render(request, 'cafe/update_user.html', {'form': form})


@login_required
def update_user_password(request):
    current_user = request.user
    try:
        customer = current_user.customer
    except Customer.DoesNotExist:
        # Handle the case where Customer doesn't exist for the user
        customer = None

    form = ChangeUserPassword(request.POST, current_user)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            # update customer
            if customer:
                customer.password = form.cleaned_data['new_password1']
                customer.save()
            messages.success(
                request, f'Hey {current_user.username}, your password has been updated !!')
            return redirect('login')
        else:
            messages.error(
                request, 'There was an error in the form. Please correct it.')
    else:
        form = ChangeUserPassword(current_user)
    return render(request, 'cafe/update_password.html', {'form': form})
