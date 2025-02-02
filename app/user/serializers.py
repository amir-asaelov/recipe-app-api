"""
Serializers for the user API view
"""
from django.contrib.auth import get_user_model

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the User object"""

    # tell ModelSerializer which 'model' it is representing
    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'name']
        extra_kwargs = {
            'password': {
                'write_only': True,
                'min_length': 5
            }
        }

    def create(self, validated_data):
        """Create and return a User with encrypted password"""
        return get_user_model().objects.create_user(**validated_data)
