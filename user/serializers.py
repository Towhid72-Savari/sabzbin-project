from rest_framework import serializers
from user.models import User, UserAddress, \
    UserScoreTransaction, UserScore


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user objects"""

    class Meta:
        model = User
        fields = ['phone', 'password', 'first_name', 'last_name',
                  'referral', 'birth_date', 'image']
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""
        user = User.objects.create_user(**validated_data)
        UserScoreTransaction.add_transactions(user_id=user.id, point_type='profile')

        if validated_data['referral']:
            referral_user = User.objects.get(phone=validated_data['referral'])
            referral_id = referral_user.id
            UserScoreTransaction.add_transactions(referral_id, 'referral')

        return user


class UserAddressDetailSerializer(serializers.ModelSerializer):
    """Serializes the specific user addressees"""

    class Meta:
        model = UserAddress
        fields = ['address', 'latitude', 'longitude']


class UserAddressListSerializer(serializers.ModelSerializer):
    """Serializes the specific user addressees"""

    class Meta:
        model = UserAddress
        fields = ['uuid', 'address', 'latitude', 'longitude']
        extra_kwargs = {'latitude': {'write_only': True},
                        'longitude': {'write_only': True}}

    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""

        return UserAddress.objects.create(user=self.context['request'].user, **validated_data)


class UserScoreSerializer(serializers.ModelSerializer):
    """Serializes the users score"""

    class Meta:
        model = UserScore
        fields = ['types', 'points']
