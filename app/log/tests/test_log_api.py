from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework import status
from django.urls import reverse
from rest_framework.test import APIClient
from log.models import Log
from log.serializers import LogSerializer


ALL_LOGS_URL = reverse('log:all_logs')


def SINGLE_LOG_URL(log_id):
    return reverse('log:single_log', args=[log_id])


class LogApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            username='teste',
            email='teste@email.com',
            password='12345678'
        )
        self.log = Log.objects.create(
            description='Log',
            details='descricao do log',
            level='DEBUG',
            origin='127.0.0.1',
            events=200,
            archived=False
        )

    def test_create_new_log_without_credentials_fail(self):
        """Teste para certificar que é impossível criar
        novo log sem estar autenticado como usuário"""
        payload = {
            'description': 'Log2',
            'details': 'descricao do log',
            'level': 'WARNING',
            'origin': '192.168.0.1',
            'events': 600,
            'archived': False
        }
        res = self.client.post(ALL_LOGS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_new_log_succesfully(self):
        """Teste de criação de novo log com sucesso
        por estar autenticado"""
        payload = {
            'description': 'Log2',
            'details': 'descricao do log',
            'level': 'WARNING',
            'origin': '192.168.0.1',
            'events': 600,
            'archived': False
        }
        self.client.force_authenticate(user=self.user)
        res = self.client.post(ALL_LOGS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertIn('id', res.data)
        self.assertIn('created_at', res.data)

    def test_create_log_invalid(self):
        """Teste criando log com entradas inválidas"""
        payload = {
            'description': 2,
            'details': '',
            'level': 'WARNING',
            'origin': '0.0.0.0',
            'events': 600,
            'archived': True
        }
        self.client.force_authenticate(user=self.user)
        res = self.client.post(ALL_LOGS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_view_all_logs_without_credentials_fail(self):
        """Teste para certificar impossibilidade de visualizar a
        lista dos logs sem ser usuário autenticado"""
        res = self.client.get(ALL_LOGS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_view_all_logs_list_succesfully(self):
        """Teste para visualização dos logs com usuário
        autenticado"""
        payload = {
            'description': 'Log2',
            'details': 'descricao do log',
            'level': 'WARNING',
            'origin': '192.168.0.1',
            'events': 600,
            'archived': False
        }
        self.client.force_authenticate(user=self.user)

        """Criando novo log primeiro pra lista ter
        múltiplos logs na listagem"""
        self.client.post(ALL_LOGS_URL, payload)
        res = self.client.get(ALL_LOGS_URL)

        logs = Log.objects.all()
        serializer = LogSerializer(logs, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
        self.assertIn('description', res.data[0])
        self.assertIn('description', res.data[1])

    def test_view_single_log_succesfully(self):
        """Teste para visualização de log por id
        com usuário autenticado"""
        self.client.force_authenticate(user=self.user)
        res = self.client.get(SINGLE_LOG_URL(self.log.id))

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['description'], 'Log')
        self.assertEqual(res.data['id'], 1)

    def test_view_single_log_without_credentials_fail(self):
        """Teste para certificar impossibilidade de visualizar a
        log com id sem autenticação"""
        res = self.client.get(SINGLE_LOG_URL(self.log.id))

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_put_log_succesfully(self):
        """Teste de alteração do log usando o verbo PUT"""
        payload = {
            'description': 'Log alterado',
            'details': 'descricao do log ALTERADA',
            'level': 'ERROR',
            'origin': '127.0.0.1',
            'events': 200,
            'archived': False
        }
        self.client.force_authenticate(user=self.user)
        res = self.client.put(SINGLE_LOG_URL(self.log.id), payload)

        self.assertEqual(res.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(res.data['id'], 1)
        self.assertEqual(res.data['description'], 'Log alterado')
        self.assertEqual(res.data['details'], 'descricao do log ALTERADA')
        self.assertEqual(res.data['level'], 'ERROR')
        self.assertEqual(res.data['origin'], '127.0.0.1')
        self.assertEqual(res.data['events'], 200)
        self.assertEqual(res.data['archived'], False)

    def test_patch_log_succesfully(self):
        payload = {
            'events': 500,
            'archived': True
        }
        self.client.force_authenticate(user=self.user)
        res = self.client.patch(SINGLE_LOG_URL(self.log.id), payload)

        self.assertEqual(res.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(res.data['id'], 1)
        self.assertEqual(res.data['description'], 'Log')
        self.assertEqual(res.data['details'], 'descricao do log')
        self.assertEqual(res.data['level'], 'DEBUG')
        self.assertEqual(res.data['origin'], '127.0.0.1')
        self.assertEqual(res.data['events'], 500)
        self.assertEqual(res.data['archived'], True)

    def test_delete_log_succesfully(self):
        self.client.force_authenticate(user=self.user)
        res = self.client.delete(SINGLE_LOG_URL(self.log.id))
        log_exists = Log.objects.filter(id=self.log.id).exists()

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(log_exists)

    def test_search_for_log_without_credentials_fail(self):
        """Teste para pesquisa de logs sem estar autenticado"""
        search_for = 'log'
        res = self.client.get(
            f'http://localhost:8000/api/logs/results?search={search_for}'
        )

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_search_for_log_with_credentials_succesfully(self):
        """Teste para pesquisa de logs por description e/ou details
        funciona corretamente e apenas autenticado"""
        self.log = Log.objects.create(
            description='Log 2',
            details='descricao do log',
            level='ERROR',
            origin='127.0.0.1',
            events=200,
            archived=False
        )
        self.log = Log.objects.create(
            description='microservice warning',
            details='microservice about to fail',
            level='WARNING',
            origin='192.168.0.1',
            events=100,
            archived=False
        )
        self.client.force_authenticate(user=self.user)
        search_for = 'microservice'
        res = self.client.get(
            f'http://localhost:8000/api/logs/results?search={search_for}'
        )

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('microservice', res.data[0]['description'])
        self.assertIn('microservice', res.data[0]['details'])
