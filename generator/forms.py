from django.forms import ModelForm, widgets, \
    formset_factory, ModelChoiceField, CharField
from generator.models import Schema, SchemaRow, DataType
from generator.repozitories import DataTypeRepozitory


class SchemaForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(SchemaForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Schema
        fields = ('name', 'column_separator', 'string_character')


class SchemaRowForm(ModelForm):

    data_type = ModelChoiceField(
        queryset=DataTypeRepozitory.get_queryset_for_selector(),
        required=True,
        widget=widgets.Select(attrs={
            'class': 'form-select data_type_select',
            'required': 'required'
        })
    )

    name = CharField(
        required=True,
        widget=widgets.TextInput(attrs={
            'class': 'form-control',
            'required': 'required'
        })
    )

    class Meta:
        model = SchemaRow
        fields = ('range_start', 'range_end', 'order')

        widgets = {
            'range_start': widgets.TextInput(attrs={
                'class': 'form-control'
            }),
            'range_end': widgets.TextInput(attrs={
                'class': 'form-control'
            }),
            'order': widgets.TextInput(attrs={
                'class': 'form-control'
            }),

        }


SchemaRowFormSet = formset_factory(SchemaRowForm, extra=1)
