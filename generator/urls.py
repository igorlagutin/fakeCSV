from django.urls import path
from generator.views import SchemaListView, CreateSchemaView, EditSchemaView
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', SchemaListView.as_view(), name="schema_list"),
    path('create', CreateSchemaView.as_view(), name="schema_create"),
    path('<int:pk>/edit', login_required(EditSchemaView.as_view()), name="schema_edit"),

]
