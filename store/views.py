from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet,GenericViewSet
# from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter,OrderingFilter
from . pagination import DefaultPagination
from rest_framework.permissions import IsAuthenticated,AllowAny,IsAdminUser,DjangoModelPermissions
from . models import *
from . serializer import *
# from . filter import ProductFilter
from rest_framework.mixins import CreateModelMixin,RetrieveModelMixin,DestroyModelMixin,UpdateModelMixin,ListModelMixin

from django.db.models import Count
from rest_framework import status
from  . permissions import IsAdminOrReadOnly,FullDjangoModelPermissions,ViewCustomerHistoryPermissions


# Create your views here.



# product fulldetails

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # filter_backends = [SearchFilter,OrderingFilter]
    pagination_class = DefaultPagination
    permission_classes =[IsAdminOrReadOnly]
    # filterset_class = ProductFilter
    search_fields = ['name']
    ordering_fields = ['offer_price','last_update']

    def get_serializer_context(self):
        return {'request':self.request}


    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id=kwargs['pk']).count()>0:
            return Response({'error':'producty cannot be deleted because it is assoiciated with an order item .'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)


# review details

class ReviewViewSet(ModelViewSet):
    queryset =Review.objects.all()
    serializer_class =ReviewSerializer




# custome details

class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class =CustomerSerializer
    permission_classes=[IsAdminUser]


    @action(detail=True,permission_classes=[ViewCustomerHistoryPermissions])
    def history(self,request,pk):
        return Response("okk")

 
    @action(detail=False ,methods=['GET','PUT'],permission_classes =[IsAuthenticated])
    def me(self,request):
    
        try:
            (customer,created) =Customer.objects.get_or_create(user_id=request.user.id)
        except Customer.DoesNotExist:
            customer=None
        if request.method =='GET':
            serializer =CustomerSerializer(customer)
            return Response(serializer.data)
        elif request.method=='PUT':
            serializer=CustomerSerializer(customer,data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)


# Category details



class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.annotate(product_count=Count('product')).all()
    serializer_class = CategorySerializer
    permission_classes =[IsAdminOrReadOnly]
    def delete(self,request,pk):
        collection = get_object_or_404(Category,pk=pk)
        if collection.products.count()>0:
            return Response({'error':'Category canot be deleted becase it includes one or more products'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

# Banner details


class BannerViewSet(ModelViewSet):
    permission_classes =[IsAdminOrReadOnly]
    queryset =Banner.objects.all()
    serializer_class =BannerSerializer


# cartprogram

class CartViewSet(CreateModelMixin,GenericViewSet,RetrieveModelMixin,DestroyModelMixin,UpdateModelMixin,ListModelMixin):
    queryset = Cart.objects.prefetch_related('items__product').all()
    serializer_class = CartSerializer
    def get_permissions(self):
        if self.request.method in ['PUT','PATCH','DELETE']:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Order.objects.all()
        try:
            customer_id = Customer.objects.only('id').get(user_id = user.id)
        except Customer.DoesNotExist:
            customer_id =None
        return Order.objects.filter(customer_id=customer_id)


class OrderViewSet(ModelViewSet):
    http_method_names=['get','post','patch','delete','head','options']

    def get_permissions(self):
        if self.request.method in ['PUT','PATCH','DELETE']:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        serializer =CreateOrderSerializer(data=request.data,context={'user_id':self.request.user.id})
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        serializer=OrderSerializer(order)
        return Response(serializer.data)


    def get_serializer_class(self):
        if self.request.method=='POST':
            return CreateOrderSerializer
        elif self.request.method=='PATCH':
            return UpdateOrderSerializer
        return OrderSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Order.objects.all()
        try:
            customer_id = Customer.objects.only('id').get(user_id = user.id)
        except Customer.DoesNotExist:
            customer_id =None
        return Order.objects.filter(customer_id=customer_id)