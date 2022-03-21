from django.shortcuts import render, redirect
from django.views.generic import ListView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from generator.services import SchemaService, SchemaRowService, DataTypeService
from generator.forms import SchemaForm, SchemaRowFormSet, SchemaEditRowFormSet


class SchemaListView(LoginRequiredMixin, ListView):
    """View that display all schemas created by current user"""
    paginate_by = 20
    context_object_name = "schemas"
    template_name = "generator/index.html"

    def get_queryset(self, **kwargs):
        service = SchemaService(self.request)
        return service.get_user_schemas()


class CreateSchemaView(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        self.has_range_list = DataTypeService.get_data_type_ids_has_range()
        return super(CreateSchemaView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        schema_form = SchemaForm(prefix="schema_form")
        schema_row_form = SchemaRowFormSet(prefix="schema_row_form")
        context = {
            'schema_form': schema_form,
            'schema_row_form': schema_row_form,
            'has_range': self.has_range_list
        }
        return render(request, 'generator/create_schema.html', context)

    def post(self, request):
        schema_form = SchemaForm(request.POST, prefix="schema_form")
        schema_row_form = SchemaRowFormSet(request.POST, prefix="schema_row_form")

        if schema_form.is_valid() and schema_row_form.is_valid():
            schema_id = SchemaService(self.request).create_schema_from_form(schema_form)
            schema_row_service = SchemaRowService(self.request)
            schema_row_service.create_schema_row_from_formset(schema_row_form.cleaned_data, schema_id)
            return redirect("schema_list")
        else:
            context = {
                'schema_form': schema_form,
                'schema_row_form': schema_row_form,
                'has_range': self.has_range_list
            }
            return render(request, 'generator/create_schema.html', context)

class EditSchemaView(View):
    def dispatch(self, request, pk, *args, **kwargs):
        self.service = SchemaService(request)
        self.schema, self.rows = self.service.get_schema_and_related_rows_by_pk(pk)
        self.has_range_list = DataTypeService.get_data_type_ids_has_range()
        return super(EditSchemaView, self).dispatch(request, pk, *args, **kwargs)

    def get(self, request, pk):
        schema_form = SchemaForm(
            instance=self.schema,
            prefix="schema_form")
        schema_row_form = SchemaEditRowFormSet(
            queryset=self.rows,
            prefix="schema_row_form"
        )
        context = {
            'has_range': self.has_range_list,
            'schema_form': schema_form,
            'schema_row_form': schema_row_form,
            'pk': pk
        }
        return render(request, 'generator/edit_schema.html', context)

    def post(self, request, pk):
        schema_form = SchemaForm(
            request.POST,
            instance=self.schema,
            prefix="schema_form")
        schema_row_form = SchemaEditRowFormSet(
            request.POST,
            queryset=self.rows,
            prefix="schema_row_form",
        )
        if schema_form.is_valid() and schema_row_form.is_valid():
            self.service.save_schema_from_form(schema_form)
            schema_row_form.save()
        else:
            context = {
                'has_range': self.has_range_list,
                'schema_form': schema_form,
                'schema_row_form': schema_row_form,
                'pk': pk
            }
            return render(request, 'generator/edit_schema.html', context)

        return redirect('schema_list')