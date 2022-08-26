from django.urls import path 
from base.views.user_views import *



urlpatterns= [
    path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('register/', registerUser.as_view(), name='register'),
    path('profile/', getUserProfile.as_view(), name="users-profile"),
    path('profile/update/', updateUserProfile.as_view(), name="user-profile-update"),
    path('', getUsers.as_view(), name="users"),
    path('delete/<str:pk>/', DeleteUser.as_view(), name='user-delete'),
    path('update/<str:pk>/', updateUser.as_view(), name='user-update'),
    path('<str:pk>/', getUserById.as_view(), name='user'),
]