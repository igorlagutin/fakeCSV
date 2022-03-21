from django.forms import ModelForm, widgets, \
    formset_factory, ModelChoiceField, CharField, \
    IntegerField, modelformset_factory, Form
from generator.models import Schema, SchemaRow
from generator.repozitories import DataTypeRepozitory


class SchemaForm(ModelForm):
    """form for create/edit schema"""
    def __init__(self, *args, **kwargs):
        super(SchemaForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Schema
        fields = ('name', 'column_separator', 'string_character')


class SchemaRowForm(ModelForm):
    """Form for create/edit schema row,
    is base for SchemaRowFormSet and SchemaEditRowFormSet"""
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
        fields = ('id','range_start', 'range_end', 'order', 'name', 'data_type')

        widgets = {
            'range_start': widgets.TextInput(attrs={
                'class': 'form-control',
                'required': 'required'
            }),
            'range_end': widgets.TextInput(attrs={
                'class': 'form-control',
                'required': 'required'
            }),
            'order': widgets.TextInput(attrs={
                'class': 'form-control'
            }),

        }


# formset for multi schema rows create
SchemaRowFormSet = formset_factory(SchemaRowForm, extra=1)

# formset for multi schema rows edit
SchemaEditRowFormSet = modelformset_factory(
    SchemaRow,
    form=SchemaRowForm,
    extra=0,
    can_delete=True
)


class GenerateDatasetForm(Form):
    """form for dataset generate """
    rows_qty = IntegerField(
        widget=widgets.TextInput()
    )
    id = IntegerField(
        widget=widgets.HiddenInput()
    )
