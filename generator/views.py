from django.shortcuts import render, redirect
from django.views.generic import ListView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from generator.services import SchemaService, SchemaRowService
from generator.forms import SchemaForm, SchemaRowFormSet


class SchemaListView(LoginRequiredMixin, ListView):
    """View that display all schemas created by current user"""
    paginate_by = 20
    context_object_name = "schemas"
    template_name = "generator/index.html"

    def get_queryset(self, **kwargs):
        service = SchemaService(self.request)
        return service.get_user_schemas()


class CreateSchema(LoginRequiredMixin, View):

    def get(self, request):
        schema_form = SchemaForm(prefix="schema_form")
        schema_row_form = SchemaRowFormSet(prefix="schema_row_form")
        context = {
            'schema_form': schema_form,
            'schema_row_form': schema_row_form,
        }
        return render(request, 'generator/create_schema.html', context)

    def post(self, request):
        schema_form = SchemaForm(request.POST, prefix="schema_form")
        schema_row_form = SchemaRowFormSet(request.POST, prefix="schema_row_form")

        if schema_form.is_valid() and schema_row_form.is_valid():
            schema_id = SchemaService(self.request).create_schema_from_form(schema_form)
            schema_row_service = SchemaRowService(self.request)
            schema_row_service.save_schema_row_formset(schema_row_form.cleaned_data, schema_id)
            print(schema_row_form.cleaned_data)
            return redirect("schema_list")

        else:
            context = {
                'schema_form': schema_form,
                'schema_row_form': schema_row_form
            }
            return render(request, 'generator/create_schema.html', context)
