from unittest import mock
from django.contrib.auth.models import Permission, User
from django.test import TestCase, RequestFactory
from django.urls import reverse


class GeneratorViewTest(TestCase):
    def setUp(self):
        self.USERNAME = 'test'
        self.PASS = '12test12'
        user = User.objects.create_user(
            username=self.USERNAME,
            password=self.PASS,
            email='test@example.com'
        ).save()

    def tearDown(self):
        User.objects.all().delete()

    def test_login_view(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_unauthenticated_schema_list_view(self):
        target_url = reverse('schema_list')
        response = self.client.get(target_url)
        self.assertRedirects(
            response,
            '/accounts/login/?next={}'.format(target_url),
            status_code=302,
            target_status_code=200
        )

    def test_authenticated_schema_list_view(self):
        self.client.login(username=self.USERNAME, password=self.PASS)
        response = self.client.get(reverse('schema_list'))
        self.assertEqual(response.status_code, 200)

    def test_unauthenticated_schema_create_view(self):
        target_url = reverse('schema_create')
        response = self.client.get(target_url)
        self.assertRedirects(
            response,
            '/accounts/login/?next={}'.format(target_url),
            status_code=302,
            target_status_code=200
        )

    def test_authenticated_schema_create_view(self):
        self.client.login(username=self.USERNAME, password=self.PASS)
        response = self.client.get(reverse('schema_create'))
        self.assertEqual(response.status_code, 200)

