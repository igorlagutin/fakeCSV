import os
import csv
import random
from faker import Faker
from django.conf import settings
from django.core.files import File
from django.core.exceptions import PermissionDenied
from generator.repozitories import SchemaRepozitory, \
    SchemaRowRepozitory, DataTypeRepozitory, GeneratorRepo


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

    def create_dataset(self, schema_pk: int) -> int:
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
        """method take list of dicts with data for create schema row and schema_pk,
        pass this data to repo to create schema row """
        for instance_data in formset:
            self.repo.create_schema_row(instance_data, schema_id)


class DataTypeService:
    """business logic related to data types"""

    @staticmethod
    def get_data_type_ids_has_range() -> list:
        "return list if data type ids that has_range=True"
        return list(DataTypeRepozitory.get_data_type_ids_has_range())


class GenerateService:
    """this class response for generating and saving
    csv file from schema data and rows qty"""

    @staticmethod
    def generate_csv(dataset_pk: int, row_qty: int) -> None:
        """generate csv file with data in data_set
        schema rows with row qty =row_qty and save it to dataset file field"""
        repo = GeneratorRepo.get_dataset_schema_and_rows_by_dataset_pk(dataset_pk)
        rows = repo['rows']
        dataset = repo['dataset']
        schema = repo['schema']

        filename = "{}_dataset_{}.csv".format(
            dataset_pk,
            dataset.created_at.strftime('%d_%m_%y')
        )
        path = str(settings.MEDIA_ROOT) + "/tmp/" + filename
        fake = Faker()
        with open(path, mode='w', newline='') as csvfile:
            fieldnames = rows.values_list("name", flat=True)
            writer = csv.DictWriter(
                csvfile,
                fieldnames=fieldnames,
                delimiter=schema.column_separator.character,
                quotechar=schema.string_character.character)
            writer.writeheader()

            for _ in range(row_qty):
                dict_with_names_and_values = {}
                for field in rows:
                    range_start = field.range_start
                    range_end = field.range_end
                    if field.data_type.name == "Integer":
                        field.value = random.randint(range_start, range_end)
                    elif field.data_type.name == "Job":
                        field.value = fake.job()
                    elif field.data_type.name == "Phone":
                        field.value = fake.phone_number()
                    elif field.data_type.name == "Email":
                        field.value = fake.email()
                    elif field.data_type.name == "Text":
                        nb_words = random.randint(range_start, range_end)
                        field.value = fake.sentence(nb_words=nb_words)
                    else:
                        field.value = field.value = fake.sentence(nb_words=5)
                    dict_with_names_and_values[field.name] = field.value
                writer.writerow(dict_with_names_and_values)
            csvfile.close()

        dataset.status = GeneratorRepo.get_dataset_status_ready()
        with open(path, mode='r', newline='') as csvfile:
            dataset.csv_file.save(filename, File(csvfile))
            csvfile.close()
        os.remove(path)