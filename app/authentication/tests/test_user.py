from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status


REGISTER_URL = reverse('authentication:register')
TOKEN_URL = reverse('authentication:token_obtain_pair')
REFRESH_TOKEN_URL = reverse('authentication:token_refresh')
ALL_USERS_URL = reverse('authentication:all_users')
def SINGLE_USER_URL(user_id):
    return reverse('authentication:single_user', args=[user_id])


class UserTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            username = 'teste',
            email = 'teste@email.com',
            password = '12345678'
        )
        self.admin = get_user_model().objects.create_superuser(
            username = 'admin',
            email = 'admin@email.com',
            password = '12345678'
        )

    def test_create_valid_user_succesfully(self):
        """Teste para criação de usuário válido"""
        payload = {
            'email': 'teste2@email.com',
            'username': 'teste2',
            'password': '12345678'
        }
        res = self.client.post(REGISTER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_already_exists(self):
        """Teste para erro quando o usuário já existe"""
        payload = {
            'email': 'teste@email.com',
            'username': 'teste',
            'password': '12345678'
        }

        """Aqui vai se tentar criar outro usuário com as mesmas credenciais 
        do 'user' criado no setUp e presentes no 'payload' acima""" 
        res = self.client.post(REGISTER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_length_validation(self):
        """Testa se o usuário não será criado caso a 
        senha seja menor que 8 caracteres"""
        payload = {
            'email': 'teste2@email.com',
            'username': 'teste2',
            'password': '1234567'
        }
        res = self.client.post(REGISTER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email = payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_token_succesfully_created(self):
        payload = {
            'email': 'teste@email.com',
            'password': '12345678'
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('access', res.data)
        self.assertIn('refresh', res.data)

    def test_token_does_not_exists(self):
        """Testa se nenhum token será criado/retornado
        caso o usuário não exista"""
        payload = {
            'email': 'inexistente@email.com',
            'password': '12345678'
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertNotIn('access', res.data)

    def test_refresh_token_returns_access_token(self):
        """Teste para o correto retorno de novo token
        de acesso na rota '/token/refresh/' """
        payload = {
            'email': 'teste@email.com',
            'password': '12345678'
        }
        res = self.client.post(TOKEN_URL, payload)

        refresh_token = res.data['refresh']
        old_access_token = res.data['access']

        payload = {
            'refresh': refresh_token
        }
        res = self.client.post(REFRESH_TOKEN_URL, payload)
        new_access_token = res.data['access']

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('access', res.data)
        self.assertNotEqual(new_access_token, old_access_token)

    def test_users_view_are_protected_for_non_users(self):
        """Testa se a view de usuário está protegida 
        contra não usuário"""
        res = self.client.get(ALL_USERS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_users_view_protected_for_common_users(self):
        """Testa se a view está protegida contra 
        usuários comuns"""
        self.client.force_authenticate(user=self.user)
        res = self.client.get(ALL_USERS_URL)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_single_user_view_protected_for_common_users(self):
        """Testa se a view está protegida contra 
        usuários comuns"""
        self.client.force_authenticate(user=self.user)
        res = self.client.get(SINGLE_USER_URL(self.user.id))

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_users_view_available_for_superusers(self):
        """Testa se um super usuário pode acessar
        corretamente a view de usuário cadastrados"""
        self.client.force_authenticate(user=self.admin)
        res = self.client.get(ALL_USERS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('email', res.data[0])

    def test_single_user_view_available_for_superusers(self):
        """Testa se um super usuário pode acessar
        corretamente a view de um usuário único"""
        self.client.force_authenticate(user=self.admin)
        res = self.client.get(SINGLE_USER_URL(self.admin.id))

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('email', res.data)
        self.assertEqual(res.data['email'], 'admin@email.com')
