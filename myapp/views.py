import datetime

from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from django.urls.base import reverse

from .forms import OrderForm, InterestForm, RegisterForm
from .models import Category, Product, Client, Order
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User


# Create your views here.
redirect = False

def index(request):
    user = request.user
    print(user)
    if str(user) != 'AnonymousUser':
        loggedIn = True
    else:
        loggedIn = False
    cat_list = Category.objects.all().order_by('id')[:10]
    print(str(request.session.keys()))
    return render(request, 'myapp/index.html', {'cat_list': cat_list,'loggedin': str(loggedIn),'user': user})


def about(request):
    user = request.user
    if str(user) != 'AnonymousUser':
        loggedIn = True
    else:
        loggedIn = False
    cookie = request.COOKIES.get('about_visits')
    response = render(request, 'myapp/about.html',{'loggedin': str(loggedIn)})
    if cookie:
        cookie = int(cookie) + 1
        response.set_cookie('about_visits', str(cookie), expires=300)
    else:
        response.set_cookie('about_visits', str(1), expires=300)

    return response


def detail(request, cat_no):
    user = request.user
    if str(user) != 'AnonymousUser':
        loggedIn = True
    else:
        loggedIn = False
    category = get_object_or_404(Category, id=cat_no)
    warehouse_location = category.warehouse
    prod_list = Product.objects.filter(category=category)
    return render(request, 'myapp/detail.html',
                  {'prod_list': prod_list, 'warehouse_loc': warehouse_location, 'cat': category,'loggedin': str(loggedIn)})


def products(request):
    user = request.user
    if str(user) != 'AnonymousUser':
        loggedIn = True
    else:
        loggedIn = False
    prodlist = Product.objects.all().order_by('id')[:10]
    return render(request, 'myapp/products.html', {'prodlist': prodlist,'loggedin': str(loggedIn)})


def place_order(request):
    user = request.user
    if str(user) != 'AnonymousUser':
        loggedIn = True
    else:
        loggedIn = False
    msg = ''
    prodlist = Product.objects.all()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['product']
            order = form.save(commit=False)
            if order.num_units <= order.product.stock:
                order.save()
                product = Product.objects.get(name=name)
                product.stock = product.stock - order.num_units
                product.save()
                msg = 'Your order has been placed successfully!!'
            else:
                msg = 'We do not have sufficient stock to fill your order!!'
            return render(request, 'myapp/order_response.html', {'msg': msg,'loggedin': str(loggedIn)})
    else:
        form = OrderForm()
    return render(request, 'myapp/placeorder.html', {'form': form, 'msg': msg, 'prodlist': prodlist,'loggedin': str(loggedIn)})


def productdetail(request, prod_id):
    user = request.user
    if str(user) != 'AnonymousUser':
        loggedIn = True
    else:
        loggedIn = False
    try:
        msg = ''
        product = Product.objects.get(id=prod_id)
        if request.method == 'GET':
            form = InterestForm()
        elif request.method == 'POST':
            form = InterestForm(request.POST)
            if form.is_valid():
                interested = form.cleaned_data['interested']
                if int(interested) == 1:
                    product.interested += 1
                    product.save()
                    return redirect(reverse('myapp:index'))
        return render(request, 'myapp/productdetail.html', {'form': form, 'msg': msg, 'product': product, 'loggedin': str(loggedIn)})
    except Product.DoesNotExist:
        msg = 'The requested product does not exist. Please provide correct product id.'
        return render(request, 'myapp/productdetail.html', {'msg': msg, 'loggedin': str(loggedIn)})


# Create your views here.
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            current_dateTime = datetime.datetime.now()
            request.session['last_login'] = str(current_dateTime)
            request.session.set_expiry(3600)
            print(request.session.keys(), request.session.values())
            if user.is_active:
                login(request, user)
                if not request.session['redirect_myorders']:
                    return HttpResponseRedirect(reverse('myapp:index'))
                else:
                    return HttpResponseRedirect(reverse('myapp:myorders'))
            else:
                return HttpResponse('Your account is disabled.')
        else:
            return HttpResponse('Invalid login details.')


def myorders(request):
    user = request.user
    if str(user) != 'AnonymousUser':
        loggedIn = True
    else:
        loggedIn = False
    if str(user) != 'AnonymousUser':
        clients = list(Client.objects.values_list('username', flat=True))
        if str(user) in clients:
            id = Client.objects.values_list('id', flat=True).filter(username=str(user))[0]
            orders = list(Order.objects.values().filter(client_id=id))
            for order in orders:
                order['name'] = Product.objects.values('name').filter(id=order['product_id'])[0]['name']
            return render(request, 'myapp/myorders.html', {'orderlist': orders, 'isClient': True, 'loggedin': str(loggedIn)})
        else:
            return render(request, 'myapp/myorders.html', {'orderlist': [], 'isClient': False, 'loggedin': str(loggedIn)})
    else:
        request.session['redirect_myorders'] = True
        request.session.set_expiry(3600)
        return render(request, 'myapp/login.html',{'loggedin': str(loggedIn)})


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('myapp:index'))


def user_register(request):
    user = request.user
    if str(user) != 'AnonymousUser':
        loggedIn = True
    else:
        loggedIn = False
    msg = ''
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return render(request, 'myapp/login.html')
    else:
        form = RegisterForm()
    return render(request, 'myapp/register.html', {'form': form, 'msg': msg, 'loggedin': str(loggedIn)})


def json(request):
    data = list(Category.objects.values())
    return JsonResponse(data, safe=False)
