from django.db import models
from decimal import Decimal
from uuid import uuid4
from django.core.validators import MinValueValidator
from django.contrib import admin
from django.conf import settings


# Create your models here.



class Banner(models.Model):
    name = models.CharField(max_length=255,blank=True,null=True)
    image = models.ImageField(upload_to='banner_images',blank=True,null=True)

    def __str__(self) -> str:
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=255,blank=True,null=True)
    image = models.ImageField(upload_to='categoty_images',blank=True,null=True)



    def __str__(self) -> str:
        return self.name

class Product(models.Model):

    UNIT_GRAM = 'g'
    UNIT_KILOGRAM = 'kg'
    UNIT_NOS = 'Nos'
    UNIT_LITER='Ltr'

    UNIT_CHOICES = [

        (UNIT_GRAM, 'Gram'),(UNIT_KILOGRAM,'Kilogram'),(UNIT_NOS,'Nos'),(UNIT_LITER,'Ltr')

    ]

    name = models.CharField(max_length=255,blank=True,null=True)
    image = models.ImageField(upload_to='product_images',blank=True,null=True)
    category = models.ForeignKey(Category,on_delete=models.PROTECT)
    price= models.DecimalField(max_digits=6,decimal_places=2,default=Decimal(0))
    offer_in_percentage=models.DecimalField(max_digits=6,decimal_places=2,default=Decimal(0))
    # offer_in_percentage= models.IntegerField()
    unit =models.CharField(choices=UNIT_CHOICES,max_length=3)
    last_update=models.DateField(auto_now_add=True)

    def _get_offer_price(self):
        final= self.price * int(self.offer_in_percentage)/ Decimal(100)
        offer_price=self. price - final
        return offer_price
    offer_price=property(_get_offer_price)


    def __str__(self) -> str:
        return self.name


class Customer(models.Model):
    phone = models.CharField(max_length=255)
    birth_date = models.DateField(null=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)

    

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

    @admin.display(ordering='user__first_name')
    def first_name(self,):
        return self.user.first_name


    @admin.display(ordering='user__last_name')
    def last_name(self,):
        return self.user.last_name


    class Meta:
        ordering = ['user__first_name', 'user__last_name']


class Order(models.Model):
    PAYMENT_STATUS_PENDING = 'P'
    PAYMENT_STATUS_COMPLETE = 'C'
    PAYMENT_STATUS_FAILED = 'F'

    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_STATUS_PENDING , 'Pending'),(PAYMENT_STATUS_COMPLETE, 'Compete'),(PAYMENT_STATUS_FAILED,'Failed')
    ]

    placed_at = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey(Customer,on_delete=models.PROTECT)
    payment_status = models.CharField(
        max_length=1, choices=PAYMENT_STATUS_CHOICES, default=PAYMENT_STATUS_PENDING)


class OrderItem(models.Model):
    order = models.ForeignKey(Order ,on_delete=models.PROTECT,related_name='items')
    product = models.ForeignKey(Product ,on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField()
    offer_price = models.DecimalField(max_digits=6,decimal_places=2)



class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    customer = models.OneToOneField(Customer,on_delete=models.CASCADE)


class Cart(models.Model):
    # id = models.UUIDField(primary_key=True,default=uuid4)
    created_at = models.DateTimeField(auto_now_add=True)



class CartItem(models.Model):
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE,related_name='items')
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])


    class Meta:
        unique_together = [['cart','product']]

    

class Review(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name='reviews')
    name =models.CharField(max_length=255)
    description =models.TextField()
    date =models.DateField(auto_now_add=True)
