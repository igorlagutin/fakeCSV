from django.shortcuts import get_object_or_404
from generator.models import Schema, SchemaRow, DataType


class SchemaRepozitory:

    def __init__(self, request):
        self.request = request

    def get_current_user_schemas(self) -> Schema:
        return Schema.objects.filter(author=self.request.user).order_by("-created_at")


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