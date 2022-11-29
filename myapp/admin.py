from django.contrib import admin
from .models import Product, Category, Client, Order
# Register your models here.
admin.site.register(Category)
admin.site.register(Order)

# Register your models here.
@admin.action(description='Add 50 items to selected Products')
def add50(modeladmin, request, queryset):
    for product in queryset:
        product.stock += 50
        product.save()

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock', 'available')
    actions = [add50]

admin.site.register(Product, ProductAdmin)


class ClientAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'city', 'Interested_list')

    def Interested_list(self, obj):
        interested_list = []
        for i in obj.interested_in.all():
            interested_list.append(i.name)
        return interested_list


admin.site.register(Client, ClientAdmin)