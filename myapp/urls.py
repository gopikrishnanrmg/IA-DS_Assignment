from django.urls import path
from myapp import views
app_name = 'myapp'
urlpatterns = [
     path(r'', views.index, name='index'),
     path(r'about/', views.about, name='about'),
     path(r'detail/<int:cat_no>', views.detail, name='detail'),
     path(r'products/', views.products, name='products'),
     path(r'place_order/', views.place_order, name='place_order'),
     path(r'products/<int:prod_id>/', views.productdetail, name='product_detail'),
]
