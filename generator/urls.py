from django.urls import path
from generator.views import SchemaListView, CreateSchemaView, \
    EditSchemaView, DatasetListView, DeleteSchemaView
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', login_required(SchemaListView.as_view()), name="schema_list"),
    path('create', login_required(CreateSchemaView.as_view()), name="schema_create"),
    path('<int:pk>/edit', login_required(EditSchemaView.as_view()), name="schema_edit"),
    path('<int:pk>/dataset', login_required(DatasetListView.as_view()), name="schema_dataset"),
    path('<int:pk>/delete', login_required(DeleteSchemaView.as_view()), name="delete_schema")

]
