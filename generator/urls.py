from django.urls import path
from generator.views import SchemaListView, CreateSchema

urlpatterns = [
    path('', SchemaListView.as_view(), name="schema_list"),
    path('create', CreateSchema.as_view(), name="schema_create"),
]
