from rest_framework import serializers
from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    """Serializer para o objecto de registro"""
    password = serializers.CharField(max_length=72, min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password']

    def validate(self, attrs):
        email = attrs.get('email', '')
        username = attrs.get('username', '')
        if not username.isalnum():
            raise serializers.ValidationError(
                'Nome de usuário deve ter apenas caracteres alfanuméricos')
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'password',
            'created_at',
            'is_staff',
            'is_superuser',
        ]
