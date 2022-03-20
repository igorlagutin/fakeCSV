from generator.repozitories import SchemaRepozitory, SchemaRowRepozitory


class SchemaService:
    def __init__(self, request):
        self.request = request
        self.repo = SchemaRepozitory(request)

    def get_user_schemas(self) -> object:
        user_schemas = self.repo.get_current_user_schemas()
        for seq_number, schema in zip(range(user_schemas.count()), user_schemas):
            schema.seq_number = seq_number + 1
        return user_schemas

    def create_schema_from_form(self, form:object) -> int:
        schema = form.save(commit=False)
        schema.author = self.request.user
        schema.save()
        return schema.id


class SchemaRowService:

    def __init__(self, request):
        self.request = request
        self.repo = SchemaRowRepozitory(request)

    def save_schema_row_formset(self, formset: dict, schema_id: int):
        for instance_data in formset:
            self.repo.create_schema_row(instance_data, schema_id)