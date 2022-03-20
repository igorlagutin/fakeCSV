from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from generator.models import Schema, ColumnSeparator, StringCharacter, DataType
from generator.repozitories import SchemaRepozitory, SchemaRowRepozitory, DataTypeRepozitory


class GeneratorSchemaRepozitoryTest(TestCase):

    def setUp(self):
        self.USERNAME_1 = 'test1'
        self.USERNAME_2 = 'test2'
        self.PASS = '12test12'
        user1 = User.objects.create_user(
            username=self.USERNAME_1,
            password=self.PASS,
            email='test1@example.com'
        )
        user2 = User.objects.create_user(
            username=self.USERNAME_2,
            password=self.PASS,
            email='test2@example.com'
        )
        col_sep = ColumnSeparator.objects.create(name="coma", character=",")
        str_char = StringCharacter.objects.create(name="single quote", character="'")
        Schema.objects.create(
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
        factory = RequestFactory()
        self.request = factory.get('/')
        self.request.user = User.objects.get(username=self.USERNAME_1)

    def tearDown(self):
        Schema.objects.all().delete()
        User.objects.all().delete()
        ColumnSeparator.objects.all().delete()
        StringCharacter.objects.all().delete()

    def test_get_current_user_schemas(self):
        repo = SchemaRepozitory(self.request)
        current_user_schemas = repo.get_current_user_schemas()
        self.assertEqual(current_user_schemas.count(), 1)
        self.assertEqual(current_user_schemas.last().name, "Shema 1")


class GeneratorDataTypeRepozitoryTest(TestCase):
    def setUp(self):
        DataType.objects.create(name="type1_visible")
        DataType.objects.create(name="type2_visible")
        DataType.objects.create(name="type3_invisible", is_visible=False)

    def tearDown(self):
        DataType.objects.all().delete()

    def test_get_queryset_for_selector_return_only_visible(self):
        queryset_for_selector = DataTypeRepozitory.get_queryset_for_selector()
        self.assertEqual(queryset_for_selector.count(), 2)
        self.assertTrue(queryset_for_selector[0].is_visible)
        self.assertTrue(queryset_for_selector[1].is_visible)


class GeneratorSchemaRowRepozitoryTest(TestCase):

    def setUp(self):
        self.USERNAME_1 = 'test1'
        self.PASS = '12test12'
        user1 = User.objects.create_user(
            username=self.USERNAME_1,
            password=self.PASS,
            email='test1@example.com'
        )
        DataType.objects.create(name="type1_visible")
        col_sep = ColumnSeparator.objects.create(name="coma", character=",")
        str_char = StringCharacter.objects.create(name="single quote", character="'")
        Schema.objects.create(
            name="Shema 1",
            column_separator=col_sep,
            string_character=str_char,
            author=user1
        )
        factory = RequestFactory()
        self.request = factory.get('/')
        self.request.user = User.objects.get(username=self.USERNAME_1)

    def tearDown(self):
        User.objects.all().delete()
        DataType.objects.all().delete()

    def test_create_schema_row(self):
        repo = SchemaRowRepozitory(self.request)

        schema_pk = Schema.objects.last().pk
        data_type = DataType.objects.last()
        dict = {
            'range_start': None,
            'range_end': None,
            'order': 0,
            'data_type': data_type,
            'name': 'Name 1'
        }

        new_row = repo.create_schema_row(dict, schema_pk)

        self.assertEqual(new_row.name, 'Name 1')
        self.assertEqual(new_row.author.username, self.USERNAME_1)
        self.assertEqual(new_row.schema.pk, schema_pk)