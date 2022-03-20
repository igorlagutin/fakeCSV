from django.shortcuts import get_object_or_404
from generator.models import Schema


class SchemaRepozitory:
    """here schemas are extracted from database, created and edited"""
    def __init__(self, request):
        self.request = request

    def get_current_user_schemas(self) -> Schema:
        return Schema.objects.filter(author=self.request.user).order_by("-created_at")
