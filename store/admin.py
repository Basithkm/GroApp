from django.contrib import admin
from . models import *
from . import models
from django.urls import reverse
from django.db.models.aggregates import Count
from django.db.models.query import QuerySet
from django.utils.html import format_html, urlencode
# Register your models here.



admin.site.register(Cart)




@admin.register(models.CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cart','product','quantity']

@admin.register(models.Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ['id','name','image']


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id','name','image']



@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id','name','image','category','price','offer_price','offer_in_percentage','unit','category_name','last_update']
    list_editable = ['offer_in_percentage']
    list_filter = ['last_update']
    list_per_page = 10
    list_select_related = ['category']
    search_fields = ['name']

    def category_name(self, product):
        return product.category.name




@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name','last_name','orders']
    list_per_page = 10
    list_select_related = ['user']
    ordering = ['user__first_name', 'user__last_name']
    search_fields = ['first_name__istartswith', 'last_name__istartswith']

    @admin.display(ordering='orders_count')
    
    def orders(self, customer):
        url = (
            reverse('admin:store_order_changelist')
            + '?'
            + urlencode({
                'customer__id': str(customer.id)
            }))
        return format_html('<a href="{}">{} Orders</a>', url, customer.orders_count)
        
        

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            orders_count=Count('order')
        )


class OrderItemInline(admin.TabularInline):
    autocomplete_fields = ['product']
    min_num = 1
    max_num = 10
    model = models.OrderItem
    extra = 0


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    autocomplete_fields = ['customer']
    inlines = [OrderItemInline]
    list_display = ['id', 'placed_at', 'payment_status','customer']
