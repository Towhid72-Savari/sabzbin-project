from django.urls import path
from user import views
from rest_framework_simplejwt import views as jwt_views


app_name = 'user'

urlpatterns = [
    path('', views.CreateUserView.as_view(), name='register'),
    path('login/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('addresses/', views.UserAddressView.as_view(), name='addresses'),
    path('addresses/<str:pk>/', views.AddressDetailView.as_view(), name='address_detail'),
    path('scores/', views.ScoresDetailView.as_view(), name='scores'),
]