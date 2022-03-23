from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from generator.models import Schema, ColumnSeparator, StringCharacter, DataType, SchemaRow
from generator.services import SchemaService, SchemaRowService
from generator.forms import SchemaForm


class GeneratorServiceTest(TestCase):

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

        Schema.objects.create(
            name="Shema 1",
            column_separator=col_sep,
            string_character=str_char,
            author=user1
        )

        DataType.objects.create(name="type_visible")

        factory = RequestFactory()
        self.request = factory.get('/')
        self.request.user = User.objects.get(username=self.USERNAME_1)

    def tearDown(self):
        Schema.objects.all().delete()
        User.objects.all().delete()
        ColumnSeparator.objects.all().delete()
        StringCharacter.objects.all().delete()
        DataType.objects.all().delete()

    def test_get_user_schemas(self):
        service = SchemaService(self.request)
        schema_list = service.get_user_schemas()
        self.assertEqual(schema_list.count(), 2)
        self.assertEqual(schema_list[0].seq_number, 1)
        self.assertEqual(schema_list[1].seq_number, 2)

    def test_create_schema_form_form(self):

        form = SchemaForm(data={
            'name': 'Schema name 2',
            'column_separator': ColumnSeparator.objects.last(),
            'string_character': StringCharacter.objects.last(),
        })
        service = SchemaService(self.request)
        created_schema_pk = service.create_schema_from_form(form)
        created_schema = Schema.objects.get(pk=created_schema_pk)
        self.assertEqual(created_schema.name, "Schema name 2")
        self.assertEqual(created_schema.author.username, self.USERNAME_1)

    # def test_save_schema_row_formset(self):
    #     data_type = DataType.objects.last()
    #     service = SchemaRowService(self.request)
    #     cleaned_form = [
    #         {'name': 'row1',
    #          'range_start': 11,
    #          'range_end': 12,
    #          'order': 0,
    #          'data_type': data_type,
    #         },
    #         {'name': 'row2',
    #          'range_start': 11,
    #          'range_end': 12,
    #          'order': 0,
    #          'data_type': data_type,
    #         }, ]
    #     schema_pk = Schema.objects.last().pk
    #     service.create_schema_row_from_formset(cleaned_form, schema_pk)
    #     self.assertEqual(SchemaRow.objects.last().name, 'row2')
