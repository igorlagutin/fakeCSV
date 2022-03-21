from django.shortcuts import get_object_or_404
from generator.models import Schema, SchemaRow, DataType
from django.core.exceptions import PermissionDenied


class SchemaRepozitory:

    def __init__(self, request):
        self.request = request

    def get_current_user_schemas(self) -> Schema:
        return Schema.objects.filter(author=self.request.user).order_by("-created_at")

    def get_schema_and_related_rows_by_pk(self, schema_pk: int) -> tuple:
        schema = get_object_or_404(Schema, pk=schema_pk)
        # if smb no author try to edit schema
        if schema.author != self.request.user:
            raise PermissionDenied()
        rows = SchemaRow.objects.filter(schema=schema)
        return schema, rows


class SchemaRowRepozitory:
    def __init__(self, request):
        self.request = request

    def create_schema_row(self, data: dict, schema_pk: int) -> object:
        new_row = SchemaRow.objects.create(
            author=self.request.user,
            schema_id=schema_pk,
            **data)

        return new_row


class DataTypeRepozitory:
    @staticmethod
    def get_queryset_for_selector() -> DataType:
        return DataType.objects.filter(is_visible=True)

    @staticmethod
    def get_data_type_ids_has_range() -> list:
        data_type_list = DataType.objects.filter(
            is_visible=True,
            has_range=True).values_list('id', flat=True)
        return data_type_list
