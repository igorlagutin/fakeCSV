from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from generator.services import SchemaService


class SchemaListView(LoginRequiredMixin, ListView):
    """View that display all schemas created by current user"""
    paginate_by = 20
    context_object_name = "schemas"
    template_name = "generator/index.html"

    def get_queryset(self, **kwargs):
        service = SchemaService(self.request)
        return service.get_user_schemas()
