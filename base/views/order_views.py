from email.headerregistry import Address
from rest_framework.views import APIView
from rest_framework.response import Response
from base.serializers import *
from base.models import *
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status
from datetime import datetime

class addOrderItems(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, *args, **kwargs):
        user= self.request.user
        data= self.request.data
        order_items= data['orderItems']
        if order_items and len(order_items) == 0:
            return Response({'detail': 'No Order Items'}, status= status.HTTP_400_BAD_REQUEST)
        else:
            # 1. Create order.
            order = Order.objects.create(
                user=user,
                paymentMethod= data['paymentMethod'],
                taxPrice= data['taxPrice'],
                shippingPrice= data['shippingPrice'],
                totalPrice= data['totalPrice'],
            )

            # 2. Create Shipping Address
            shipping= ShippingAddress.objects.create(
                order= order,
                address= data['shippingAddress']['address'],
                city= data['shippingAddress']['city'],
                country= data['shippingAddress']['country'],
                postalCode= data['shippingAddress']['postalCode'],
                shippingPrice= data['shippingPrice']
            )

            # 3. Create order items and set set order to order item relationship
            for i in order_items:
                product = Product.objects.get(_id=i['product'])

                item= OrderItem.objects.create(
                    product=product,
                    order= order,
                    name= product.name,
                    qty= i['qty'],
                    price= i['price'],
                    image= product.image.url,
                )

                # 4. Update stock
                product.countInStock-= i['qty']
                product.save()

                serializer= OrderSerializer(order, many=False)
                return Response(serializer.data)

class getMyOrders(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        user = self.request.user
        orders = user.order_set.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)


class getOrderById(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, pk, *args, **kwargs):
        user= self.request.user
        try:
            order= Order.objects.get(_id=pk)
            
            if user.is_staff or order.user == user:
                serializer= OrderSerializer(order, many=False)
                return Response(serializer.data)
            else:
                return Response({'detail': 'Not authorized to view this order'}, status= status.HTTP_400_BAD_REQUEST)    
        except:
            return Response({'detail': 'Order does not exists'}, status= status.HTTP_400_BAD_REQUEST)

class updateOrderToPaid(APIView):
    permission_classes = (IsAuthenticated,)
    def put(self, request, pk):
        order= Order.objects.get(_id=pk)
        order.isPaid = True
        order.paidAt= datetime.now()
        order.save()
        serializer= OrderSerializer(order, many=False)
        return Response(serializer.data)

class updateOrderToDelivered(APIView):
    permission_classes = (IsAdminUser,)
    def put(self, request, pk):
        order= Order.objects.get(_id=pk)
        order.isDelivered = True
        order.deliveredAt= datetime.now()
        order.save()
        serializer= OrderSerializer(order, many=False)
        return Response(serializer.data)

class getOrders(APIView):
    permission_classes = (IsAdminUser,)
    def get(self, requset):
        orders= Order.objects.all()
        serializer= OrderSerializer(orders, many=True)
        return Response(serializer.data)