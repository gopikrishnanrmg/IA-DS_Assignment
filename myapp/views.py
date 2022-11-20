from django.http import HttpResponse
from django.urls.base import reverse

from .forms import OrderForm, InterestForm
from .models import Category, Product
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render


# Create your views here.

def index(request):
    cat_list = Category.objects.all().order_by('id')[:10]
    return render(request, 'myapp/index.html', {'cat_list': cat_list})

def about(request):
    return render(request, 'myapp/about.html')

def detail(request, cat_no):
    category = get_object_or_404(Category, id=cat_no)
    warehouse_location = category.warehouse
    prod_list = Product.objects.filter(category=category)
    return render(request, 'myapp/detail.html', {'prod_list': prod_list, 'warehouse_loc': warehouse_location, 'cat': category})

def products(request):
    prodlist = Product.objects.all().order_by('id')[:10]
    return render(request,'myapp/products.html',{'prodlist':prodlist})


def place_order(request):
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
            return render(request, 'myapp/order_response.html', {'msg': msg})
    else:
        form = OrderForm()
    return render(request, 'myapp/placeorder.html', {'form': form, 'msg': msg, 'prodlist': prodlist})

def productdetail(request, prod_id):
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
        return render(request, 'myapp/productdetail.html', {'form': form, 'msg': msg, 'product': product})
    except Product.DoesNotExist:
        msg = 'The requested product does not exist. Please provide correct product id.'
        return render(request, 'myapp/productdetail.html', {'msg': msg})
