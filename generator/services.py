from django.core.exceptions import PermissionDenied
from generator.repozitories import SchemaRepozitory, SchemaRowRepozitory, DataTypeRepozitory


class SchemaService:
    def __init__(self, request):
        self.request = request
        self.repo = SchemaRepozitory(request)

    def get_user_schemas(self) -> object:
        user_schemas = self.repo.get_current_user_schemas()
        for seq_number, schema in zip(range(user_schemas.count()), user_schemas):
            schema.seq_number = seq_number + 1
        return user_schemas

    def create_schema_from_form(self, form: object) -> int:
        schema = form.save(commit=False)
        schema.author = self.request.user
        schema.save()
        return schema.id

    def save_schema_from_form(self, form: object) -> None:
        schema = form.save(commit=False)
        if schema.author != self.request.user:
            raise PermissionDenied()
        schema.save()

    def get_schema_and_related_rows_by_pk(self, schema_pk: int) -> tuple:
        return self.repo.get_schema_and_related_rows_by_pk(schema_pk)

class SchemaRowService:

    def __init__(self, request):
        self.request = request
        self.repo = SchemaRowRepozitory(request)

    def create_schema_row_from_formset(self, formset: list, schema_id: int):
        for instance_data in formset:
            self.repo.create_schema_row(instance_data, schema_id)

    def save_schema_row_formset(self, instances: list, rows_before_save: list) -> None:
        print('instances', instances)
        print('rows', rows_before_save)
        for row in rows_before_save:
            if row not in instances:
                row.delete()
        for instance in instances:
            instance.save()


class DataTypeService:
    @staticmethod
    def get_data_type_ids_has_range() -> list:
        return list(DataTypeRepozitory.get_data_type_ids_has_range())
