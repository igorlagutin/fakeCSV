from celery import shared_task
from generator.services import GenerateService


@shared_task()
def create_csv(dataset_pk: int, row_qty: int) -> None:
    GenerateService.generate_csv(dataset_pk, row_qty)