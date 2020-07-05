from rest_framework.pagination import CursorPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from user import serializers, models


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""
    serializer_class = serializers.UserSerializer


class UserAddressView(generics.ListCreateAPIView):
    """Listing user addresses"""
    pagination_class = CursorPagination
    permission_classes = (IsAuthenticated, )
    serializer_class = serializers.UserAddressListSerializer
    queryset = models.UserAddress.objects.values('address')

    def get_queryset(self):
        return models.UserAddress.objects.filter(user=self.request.user)


class AddressDetailView(generics.RetrieveUpdateDestroyAPIView):
    """get, put, patch, delete for a detailed address"""
    permission_classes = (IsAuthenticated,)
    queryset = models.UserAddress.objects.all()
    serializer_class = serializers.UserAddressDetailSerializer


class ScoresDetailView(generics.ListAPIView):
    """Retrieve the user scores"""
    permission_classes = (IsAuthenticated, )
    queryset = models.UserScore.objects.all()
    serializer_class = serializers.UserScoreSerializer

    def get_queryset(self):
        return models.UserScore.objects.filter(user=self.request.user)
