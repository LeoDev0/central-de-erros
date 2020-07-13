from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Sobrescrevendo a classe padrão de autenticação do JWT e 
    adicionando dados do usuário na resposta juntamente com os tokens"""    
    def validate(self, attrs):
        token = super().validate(attrs)
        # refresh = self.get_token(self.user)

        # token["refresh"] = str(refresh)
        # token["access"] = str(refresh.access_token)

        token['id'] = self.user.id
        token['username'] = self.user.username
        token["email"] = self.user.email
        token["created_at"] = self.user.created_at
        token['is_staff'] = self.user.is_staff
        token['is_superuser'] = self.user.is_superuser
        
        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
