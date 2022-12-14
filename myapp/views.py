import datetime

from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from django.urls.base import reverse

from .forms import OrderForm, InterestForm, RegisterForm, Password_ResetForm
from .models import Category, Product, Client, Order
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.core.mail import send_mail, BadHeaderError
import random
import string
from django.template.loader import render_to_string


# Create your views here.

def index(request):
    user = request.user
    print(user)
    if str(user) != 'AnonymousUser':
        loggedIn = True
    else:
        loggedIn = False
    try:
        avatar = Client.objects.values('avatar').filter(first_name=user.first_name)[0]['avatar']
    except Exception:
        avatar = ''
    cat_list = Category.objects.all().order_by('id')[:10]
    print(str(request.session.keys()))
    return render(request, 'myapp/index.html', {'cat_list': cat_list,'loggedin': str(loggedIn),'user': user, 'avatar': 'media/'+avatar})


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
                if not request.session.keys().__contains__('redirect_myorders'):
                    return HttpResponseRedirect(reverse('myapp:index'))
                else:
                    del request.session['redirect_myorders']
                    return HttpResponseRedirect(reverse('myapp:myorders'))
            else:
                return HttpResponse('Your account is disabled.')
        else:
            return HttpResponse('Invalid login details.')
    else:
        return render(request, 'myapp/login.html', {'loggedin': str(False)})

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
        form = RegisterForm(request.POST, request.FILES)
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

def password_reset(request):
    if request.method == 'POST':
        email = request.POST['email']
        user = User.objects.filter(email=email)
        print(user)
        if user:
            user = user[0]
            new_password = generate_password()
            user.set_password(new_password)
            user.save()

            print(new_password)

            # Email settings
            subject = "New Password"
            email_template_name = "myapp/password_reset_email.txt"
            c = {
                "email": user.email,
                'domain': '127.0.0.1:8000',
                'site_name': 'Website',
                "user": user,
                'protocol': 'http',
                'new_password': new_password,
            }
            email = render_to_string(email_template_name, c)
            try:
                send_mail(subject, email, 'websiteaccforme@gmail.com', [user.email], fail_silently=False)
            except BadHeaderError:
                return HttpResponse('Invalid header found.')

            return render(request, 'myapp/password_reset_done.html', {'done': "true"})
        else:
            return render(request, 'myapp/password_reset_done.html', {'done': "false"})
    else:
        if request.user.is_authenticated:
            return redirect(reverse('myapp:myorders'))
        password_reset_form = Password_ResetForm()
        return render(request, 'myapp/password_reset.html', {'form': password_reset_form})
    
def password_reset_done(request, done):
    print(done)
    return render(request, 'myapp/password_reset_done.html', {'done': done})

def generate_password():
    characters = list(string.ascii_letters + string.digits + "!@#$%^&*()")
    password_length = 8
    random.shuffle(characters)

    password = []
    for i in range(password_length):
        password.append(random.choice(characters))

    random.shuffle(password)
    return "".join(password)