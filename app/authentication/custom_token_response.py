from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Sobrescrevendo a classe padrão de autenticação do JWT e 
    adicionando dados do usuário na resposta juntamente com os tokens"""    
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)

        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)

        data['id'] = self.user.id
        data['username'] = self.user.username
        data["email"] = self.user.email
        data["created_at"] = self.user.created_at
        data['is_staff'] = self.user.is_staff
        data['is_superuser'] = self.user.is_superuser
        
        return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
