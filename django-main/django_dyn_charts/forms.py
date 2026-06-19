from django import forms
from django_dyn_charts.models import ChartsConfig

from cli.h_code_parser import name_to_class

from pprint import pp 

# Create your forms here.


class ChartConfigForm(forms.ModelForm):
    class Meta:
        model = ChartsConfig
        exclude = ('id', 'user', 'status', 'errInfo', 'prop1_values', 'prop2_values', 'prop3_values', 'prop4_values', 'prop5_values', 'prop6_values', 'prop1_label', 'prop2_label', 'prop3_label', 'prop4_label', 'prop5_label', 'prop6_label' )
    

    def __init__(self, *args, **kwargs):

        super(ChartConfigForm, self).__init__(*args, **kwargs)

        #print( '> FORM args: ' + str(args) )
        #print( '> FORM kwargs: ' + str(kwargs) )

        if 'initial' in kwargs and 'model_name' in kwargs['initial']:
            self.fields['model_name'].initial = kwargs['initial']['model_name']

        try:

            model_name = self.fields['model_name'].initial

            model_class = name_to_class( model_name ) 

            if model_class:
                
                model_fields = [(field.name, field.name) for field in model_class._meta.get_fields()]

                # Id is useledd 
                model_fields.remove( ('id', 'id') )

                for i in range(1, 7):
                    prop_field = f'prop{i}'
                    if prop_field in self.fields:
                        self.fields[prop_field].widget = forms.Select(choices=model_fields)

        except:
            pass

        for field_name, field in self.fields.items():

            #print( ' > field_name: ' + field_name + '=' + str( self.fields[field_name].initial ) ) 
            self.fields[field_name].widget.attrs['class'] = 'form-control'
            self.fields[field_name].widget.attrs['placeholder'] = field.label
        
        self.fields['description'].widget.attrs['rows'] = 3
        description_field = self.fields.pop('description')
        self.fields['description'] = description_field