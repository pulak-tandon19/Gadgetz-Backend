from django.urls import path 
from base.views.product_views import *



urlpatterns= [
    path('', getProducts.as_view(), name="products"),
    path('create/', createProduct.as_view(), name= 'create-product'),
    path('upload/', uploadImage.as_view(), name='image-upload'),
    path('top/', getTopProducts.as_view(), name='top-products'),
    path('<str:pk>/', getProduct.as_view(), name="product"),
    path('<str:pk>/reviews/', createProductReview.as_view(), name="create-review"),
    path('delete/<str:pk>/', deleteProduct.as_view(), name="product-delete"),
    path('update/<str:pk>/', updateProduct.as_view(), name="product-update"),
]