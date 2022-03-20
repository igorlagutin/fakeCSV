from generator.repozitories import SchemaRepozitory


class SchemaService:
    def __init__(self, request):
        self.request = request
        self.repo = SchemaRepozitory(request)

    def get_user_schemas(self) -> object:
        user_schemas = self.repo.get_current_user_schemas()
        for seq_number, schema in zip(range(user_schemas.count()), user_schemas):
            schema.seq_number = seq_number + 1
        return user_schemas
