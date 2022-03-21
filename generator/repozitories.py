from django.shortcuts import get_object_or_404
from generator.models import Schema, SchemaRow, DataType, DataSet, DataSetStatus
from django.core.exceptions import PermissionDenied


class SchemaRepozitory:
    """methods related to getting Schema information from database"""
    def __init__(self, request):
        self.request = request

    def _get_schema_by_pk(self, schema_pk: int) -> Schema:
        """get schema by pk,
        if schema exist - return 404 not found exception
        if schema author is not current user return 403 Forbidden exception"""
        schema = get_object_or_404(Schema, pk=schema_pk)
        # if smb no author try to edit schema
        if schema.author != self.request.user:
            raise PermissionDenied()
        return schema

    def get_current_user_schemas(self) -> Schema:
        """get all schemas where author is current user"""
        return Schema.objects.filter(author=self.request.user).order_by("-created_at")

    def get_schema_and_related_rows_by_pk(self, schema_pk: int) -> tuple:
        """get single schema by pk and all schema rows where schema == current schema"""
        schema = self._get_schema_by_pk(schema_pk)
        # if smb no author try to edit schema
        if schema.author != self.request.user:
            raise PermissionDenied()
        rows = SchemaRow.objects.filter(schema=schema)
        return schema, rows

    def get_schema_datasets_by_pk(self, schema_pk: int) -> object:
        """get single schema by pk and all data sets where schema == current schema"""
        schema = self._get_schema_by_pk(schema_pk)
        return DataSet.objects.filter(schema=schema).order_by("created_at")

    def create_dataset(self, schema_pk:int) -> int:
        """create dataset with default status and schema by pk """
        dataset = DataSet.objects.create(
            status=DataSetStatus.objects.first(),
            schema=self._get_schema_by_pk(schema_pk)
        )
        return dataset.pk

class SchemaRowRepozitory:
    """repo for db actions with SchemaRow"""
    def __init__(self, request):
        self.request = request

    def create_schema_row(self, data: dict, schema_pk: int) -> object:
        """method take dict with data for create schema row and schema_pk,
        creates schema row adding schema and request.user as author"""
        new_row = SchemaRow.objects.create(
            author=self.request.user,
            schema_id=schema_pk,
            **data)

        return new_row


class DataTypeRepozitory:
    """repo for db actions with DataTypes"""
    @staticmethod
    def get_queryset_for_selector() -> DataType:
        """return queryset for fill selector in form with data type"""
        return DataType.objects.filter(is_visible=True)

    @staticmethod
    def get_data_type_ids_has_range() -> list:
        """return list of id data types that have
            is_visble and has_range - true
         used on UI to display/hide range inputs"""
        data_type_list = DataType.objects.filter(
            is_visible=True,
            has_range=True).values_list('id', flat=True)
        return data_type_list