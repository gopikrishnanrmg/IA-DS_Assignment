from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Category, Product, Client, Order


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
