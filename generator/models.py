from django.db import models
from django.contrib.auth.models import User


class ColumnSeparator(models.Model):
    """column separators for schema"""
    character = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    is_visible = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Column Separator"
        verbose_name_plural = "Column Separators"


class StringCharacter(models.Model):
    """string quote chars for schema"""
    character = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    is_visible = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "String Character"
        verbose_name_plural = "String Characters"


class DataType(models.Model):
    """data types for csv column for example:
     Full Name, Text, Phone ... """
    name = models.CharField(max_length=100)
    has_range = models.BooleanField(
        default=False,
        help_text="use this option if data type has range"
    )
    default_content = models.CharField(max_length=1000)
    is_visible = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Data Type"
        verbose_name_plural = "Data Types"


class Schema(models.Model):
    """Data schema main data, data schema is Foreign key for data row,
    data schema is displayed with data rws"""
    name = models.CharField(max_length=100)
    column_separator = models.ForeignKey(ColumnSeparator, on_delete=models.CASCADE)
    string_character = models.ForeignKey(StringCharacter, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        pass

    class Meta:
        verbose_name = "Schema"
        verbose_name_plural = "Schemas"


class SchemaRow(models.Model):
    """Schema rows with data type and name - data for cvs columns in data schema"""
    name = models.CharField(max_length=100)
    data_type = models.ForeignKey(DataType, on_delete=models.PROTECT)
    range_start = models.IntegerField(null=True, blank=True)
    range_end = models.IntegerField(null=True, blank=True)
    order = models.IntegerField(null=True, blank=True, default=0)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    schema = models.ForeignKey(Schema, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Schema Row"
        verbose_name_plural = "Schema Rows"


class DataSetStatus(models.Model):
    """status of Dataset csv generation: processing and ready"""
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Status"
        verbose_name_plural = "Statuses"


class DataSet(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    schema = models.ForeignKey(Schema, on_delete=models.CASCADE)
    status = models.ForeignKey(DataSetStatus, on_delete=models.CASCADE)
    csv_file = models.FileField(null=True, upload_to='csv_datasets/')

    def __str__(self):
        return str(self.created_at)

    class Meta:
        verbose_name = "Data set"
        verbose_name_plural = "Data sets"
