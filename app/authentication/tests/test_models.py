from django.test import TestCase
from django.contrib.auth import get_user_model


class AuthenticationModelTests(TestCase):

    def test_create_user_with_email_succesfully(self):
        """Teste para criar novo usuário com o user model
        customizado (username, email, password)"""
        username = 'usuario'
        email = 'usuario@email.com'
        password = '12345678'
        user = get_user_model().objects.create_user(
            username=username,
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertEqual(user.username, username)
        self.assertTrue(user.check_password(password))

    def test_normalize_user_email(self):
        """Teste para saber se o email está sendo
        sanitizado/normalizado corretamente"""
        username = 'usuario'
        email = 'usuario@EMAIL.COM'
        password = '12345678'
        user = get_user_model().objects.create_user(
            username=username,
            email=email,
            password=password
        )

        self.assertEqual(user.email, email.lower())

    def test_create_new_superuser(self):
        """Teste para criação de novo super usuário"""
        username = 'superuser'
        email = 'superuser@email.COM'
        password = '12345678'
        user = get_user_model().objects.create_superuser(
            username=username,
            email=email,
            password=password
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
