from django.urls import path
from django.views.generic import TemplateView
from generator.views import SchemaListView

urlpatterns = [
    path('', SchemaListView.as_view(), name="index")
]
