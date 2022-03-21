from unittest import mock
from django.contrib.auth.models import Permission, User
from django.test import TestCase, RequestFactory
from django.urls import reverse
from generator.models import Schema, ColumnSeparator, StringCharacter


class GeneratorViewTest(TestCase):
    def setUp(self):
        self.USERNAME = 'test'
        self.USERNAME2 = 'test2'
        self.PASS = '12test12'
        user1 = User.objects.create_user(
            username=self.USERNAME,
            password=self.PASS,
            email='test@example.com'
        )

        user2 = User.objects.create_user(
            username=self.USERNAME2,
            password=self.PASS,
            email='test@example.com'
        )

        col_sep = ColumnSeparator.objects.create(name="coma", character=",")
        str_char = StringCharacter.objects.create(name="single quote", character="'")
        self.schema_by_user_1 = Schema.objects.create(
            name="Shema 1",
            column_separator=col_sep,
            string_character=str_char,
            author=user1
        )
        Schema.objects.create(
            name="Shema 2",
            column_separator=col_sep,
            string_character=str_char,
            author=user2
        )

    def tearDown(self):
        Schema.objects.all().delete()
        ColumnSeparator.objects.all().delete()
        StringCharacter.objects.all().delete()
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

    def test_unauthenticated_schema_edit_view(self):
        target_url = reverse('schema_edit', kwargs={"pk": self.schema_by_user_1.pk})
        response = self.client.get(target_url)
        self.assertRedirects(
            response,
            '/accounts/login/?next={}'.format(target_url),
            status_code=302,
            target_status_code=200
        )

    def test_authenticated_schema_edit_view(self):
        target_url = reverse('schema_edit', kwargs={"pk": self.schema_by_user_1.pk})
        self.client.login(username=self.USERNAME, password=self.PASS)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 200)

    def test_authenticated_schema_edit_by_wrong_user(self):
        target_url = reverse('schema_edit', kwargs={"pk": self.schema_by_user_1.pk})
        self.client.login(username=self.USERNAME2, password=self.PASS)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 403)