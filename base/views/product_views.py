from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from base.serializers import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from base.models import *
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status
from django.core.paginator import Paginator, EmptyPage, Page, PageNotAnInteger
import cloudinary.uploader

class getProducts(APIView):
    def get(self, *args, **kwargs):
        query= self.request.query_params.get('keyword')
        if query == None:
            query = ''

        products= Product.objects.filter(name__icontains=query)
        filter = self.request.query_params.get('filter')
        if filter == 1:
            products.order_by('-createdAt')
        elif filter == 2:
            products.order_by('price')
        elif filter == 3:
            products.order_by('price')
        page= self.request.query_params.get('page')
        paginator= Paginator(products, 4)

        try:
            products= paginator.page(page)
        except PageNotAnInteger:
            products=paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)

        if page == None:
            page=1
        page = int(page)

        serializer= ProductSerializer(products, many=True)
        return Response({'products': serializer.data, 'page': page, 'pages': paginator.num_pages})

class getTopProducts(APIView):
    def get(self, request):
        products= Product.objects.filter(rating__gte=4).order_by('-rating')[0:5]
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

class getProduct(APIView):
    # permission_classes = (IsAdminUser,)

    def get(request, self, pk):
        product= Product.objects.get(_id=pk)
        serializer= ProductSerializer(product, many=False)
        return Response(serializer.data)

class deleteProduct(APIView):
    permission_classes = (IsAdminUser,)
    def delete(request, self, pk):
        product= Product.objects.get(_id=pk)
        product.delete()
        return Response('Product Deleted!')

class createProduct(APIView):
    permission_classes = (IsAdminUser,)

    def post(self, *args, **kwargs):
        user = self.request.user

        product = Product.objects.create(
        user=user,
        name='Sample Name',
        price=0,
        brand='Sample Brand',
        countInStock=0,
        category='Sample Category',
        description=''
    )

        serializer = ProductSerializer(product, many=False)
        return Response(serializer.data)

class updateProduct(APIView):
    permission_classes = (IsAdminUser,)

    def put(self, request, pk):
        data=self.request.data
        product= Product.objects.get(_id=pk)
        product.name= data['name']
        product.price= data['price']
        product.brand= data['brand']
        product.countInStock= data['countInStock']
        product.category= data['category']
        product.description= data['description']
        product.save()

        serializer= ProductSerializer(product, many=False)
        return Response(serializer.data)

class uploadImage(APIView):
    permission_classes = (IsAdminUser,)

    def post(self, request):
        data= self.request.data
        product_id= data['product_id']
        product= Product.objects.get(_id= product_id)
        product.image= self.request.FILES.get('image')
        photo= self.request.FILES.get('image')
        cloudinary.uploader.upload(photo)
        product.save()
        return Response('Image uploaded!')

class createProductReview(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, pk):
        user= self.request.user
        product= Product.objects.get(_id=pk)
        data= self.request.data

        # 1. Review already exists.
        alreadyExists= product.review_set.filter(user=user).exists()
        if alreadyExists:
            content={'details': 'Product already reviewed!'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        # 2. No rating or 0.
        elif data['rating']==0:
            content= {'details' : 'Please select a rating'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        # 3. Create Review
        else:
            review = Review.objects.create(
                user=user,
                product=product,
                name= user.first_name,
                rating= data['rating'],
                comment= data['comment'],
            )

            reviews=product.review_set.all()
            product.numReviews= len(reviews)

            total = 0
            for i in reviews:
                total+= i.rating

            product.rating= total/len(reviews)
            product.save()
            return Response('Review Added')






       

