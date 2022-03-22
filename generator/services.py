from django.core.exceptions import PermissionDenied
from generator.repozitories import SchemaRepozitory, SchemaRowRepozitory, DataTypeRepozitory


class SchemaService:
    """business logic related to schemas"""
    def __init__(self, request):
        self.request = request
        self.repo = SchemaRepozitory(request)

    def get_user_schemas(self) -> object:
        """return all schemas where author is request.user
        and add sequence numbers for schemas"""
        user_schemas = self.repo.get_current_user_schemas()
        for seq_number, schema in zip(range(user_schemas.count()), user_schemas):
            schema.seq_number = seq_number + 1
        return user_schemas

    def create_schema_from_form(self, form: object) -> int:
        """create schema from form and add request.user as author"""
        schema = form.save(commit=False)
        schema.author = self.request.user
        schema.save()
        return schema.id

    def save_schema_from_form(self, form: object) -> None:
        """saves schema from form and check if author is request.user
        otherwise raise exception 403 Forbidden
        """
        schema = form.save(commit=False)
        if schema.author != self.request.user:
            raise PermissionDenied()
        schema.save()

    def get_schema_and_related_rows_by_pk(self, schema_pk: int) -> tuple:
        """return schema and all related schema rows by schema pk"""
        return self.repo.get_schema_and_related_rows_by_pk(schema_pk)

    def get_schema_dataset_by_pk(self, schema_pk: int) -> object:
        """get dataset from repo and add sequence number to items"""
        dataset = self.repo.get_schema_datasets_by_pk(schema_pk)
        for seq_number, item in zip(range(len(dataset)), dataset):
            item.seq_number = seq_number + 1
        return dataset

    def create_dataset(self, schema_pk:int) -> int:
        """create dataset with default status and schema by pk """
        return self.repo.create_dataset(schema_pk)

    def delete_schema_by_pk(self, schema_pk: int) -> None:
        """delete schema and related rows and datasets by schema pk"""
        self.repo.delete_schema_by_pk(schema_pk)


class SchemaRowService:
    """business logic related to schema rows"""
    def __init__(self, request):
        self.request = request
        self.repo = SchemaRowRepozitory(request)

    def create_schema_row_from_formset(self, formset: list, schema_id: int):
        for instance_data in formset:
            self.repo.create_schema_row(instance_data, schema_id)

    def save_schema_row_formset(self, instances: list, rows_before_save: list) -> None:
        for row in rows_before_save:
            if row not in instances:
                row.delete()
        for instance in instances:
            instance.save()


class DataTypeService:
    """business logic related to data types"""
    @staticmethod
    def get_data_type_ids_has_range() -> list:
        return list(DataTypeRepozitory.get_data_type_ids_has_range())
