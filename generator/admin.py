from django.contrib import admin
from generator.models import ColumnSeparator, StringCharacter, \
    DataType, Schema, SchemaRow, DataSetStatus, DataSet

admin.site.register(ColumnSeparator)
admin.site.register(StringCharacter)
admin.site.register(DataType)
admin.site.register(Schema)
admin.site.register(SchemaRow)
admin.site.register(DataSetStatus)
admin.site.register(DataSet)
