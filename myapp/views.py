from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Category, Product, Client, Order


# Create your views here.
def index(request):
    count = 1
    cat_list = Category.objects.all().order_by('id')[:10]
    prod_list = Product.objects.all().order_by('-price')[:5]
    response = HttpResponse()
    heading1 = '<p>' + 'List of categories: ' + '</p>'
    response.write(heading1)
    for category in cat_list:
        para = '<p>' + str(category.id) + ': ' + str(category) + '</p>'
        response.write(para)
    response.write('<br><br>')
    heading2 = '<p>' + 'List of products: ' + '</p>'
    response.write(heading2)
    for product in prod_list:
        response.write('<p>' + str(count) + ': ' + str(product) + '</p>')
        count += 1
    return response


def about(request):
    response = HttpResponse()
    response.write('<p> This is an Online Store APP. </p>')
    return response


def detail(request, cat_no):
    response = HttpResponse()
    category = get_object_or_404(Category, id=cat_no)
    warehouse_location = category.warehouse
    prod_list = Product.objects.filter(category=category)
    response.write('<p>' + 'The location is '+ warehouse_location + '</p> <br>')
    for i in prod_list:
        response.write('<p>' + str(i) + '</p>')
    return response

