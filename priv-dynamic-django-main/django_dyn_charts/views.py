import re, json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import HttpResponse
from django.utils.safestring import mark_safe
from django.db import models
from django.apps import apps
from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT
from django.conf import settings
from django.http import JsonResponse
from django.template import Template, Context
from itertools import zip_longest
from django_dyn_charts.forms import ChartConfigForm

from .models import *

from pprint import pp 

from cli import *

# Create your views here.

def index(request):
    
    context = {
        'routes' : settings.DYNAMIC_CHARTS.keys()
    }

    return render(request, 'pages/dynamic-charts.html', context)

def embed(request, aId):
    
    context = {} 
    user = get_user('test')

    chart_selected = chart_by_id( aId ) 
    if not chart_selected:
        return HttpResponse('> Err')

    print( ' > Selected: ' + str( chart_selected.id ) ) 
    chart_processed = process_chart( chart_selected )        

    chart_ctx  = { }
    chart_ctx['chart' ] = chart_processed

    tmpl_js = None 
    if chart_processed.type == ChartTypes.BAR:
        tmpl_js = 'js_bar.html' 
        chart_ctx['chart_js_title' ] = chart_processed.description
        chart_ctx['chart_js_label' ] = chart_processed.prop2_label
        chart_ctx['chart_js_x' ] = chart_processed.prop1_values
        chart_ctx['chart_js_y' ] = chart_processed.prop2_values
    elif chart_processed.type == ChartTypes.LINE:
        tmpl_js = 'js_line.html'
        chart_ctx['chart_js_title' ] = chart_processed.description
        chart_ctx['chart_js_label' ] = chart_processed.prop2_label
        chart_ctx['chart_js_x' ] = chart_processed.prop1_values
        chart_ctx['chart_js_y' ] = chart_processed.prop2_values
    elif chart_processed.type == ChartTypes.AREA: # NOT_DONE
        tmpl_js = 'js_area.html'
        chart_ctx['chart_title' ] = chart_processed.description
        chart_ctx['labels'   ] = chart_processed.prop1_values
        chart_ctx['data'     ] = chart_processed.prop2_values
    elif chart_processed.type == ChartTypes.COLUMN:
        tmpl_js = 'js_column.html' 
        '''
            'data_series': {'2024-09-01': {'Canada': 0, 'Germany': 0, 'USA': 1},
                '2024-09-03': {'Canada': 1, 'Germany': 0, 'USA': 0},
                '2024-09-05': {'Canada': 0, 'Germany': 1, 'USA': 1},
                '2024-09-06': {'Canada': 0, 'Germany': 0, 'USA': 1}}}
        '''
        data_series = chart_processed.data_series
        chart_ctx['x_data'] = list( data_series.keys() )
        data_series_processed = {}

        # Insert empty lists
        for k in data_series.keys():
            for j in data_series[k].keys():
                data_series_processed[ j ] = []

        # Insert data in lists
        for k in data_series.keys():
            for j in data_series[k].keys():
                data_series_processed[ j ].append(data_series[k][j]) 

        chart_ctx['data_series'  ] = data_series_processed

    elif chart_processed.type == ChartTypes.PIE:
        tmpl_js = 'js_pie.html' 
        chart_ctx['chart_js_labels'] = chart_processed.prop1_values
        chart_ctx['chart_js_data'  ] = chart_processed.prop2_values
    elif chart_processed.type == ChartTypes.DONUT:
        tmpl_js = 'js_donut.html' 
        chart_ctx['chart_js_labels'] = chart_processed.prop1_values
        chart_ctx['chart_js_data'  ] = chart_processed.prop2_values
    elif chart_processed.type == ChartTypes.RADIAL:
        tmpl_js = 'js_radial.html' 
        chart_ctx['labels'   ] = chart_processed.prop1_values
        chart_ctx['data'     ] = chart_processed.prop2_values
        chart_ctx['data_sum' ] = sum( chart_processed.prop2_values )
    elif chart_processed.type == ChartTypes.RADAR:
        tmpl_js = 'js_radar.html' 
        chart_ctx['labels' ] = chart_processed.prop1_values
        chart_ctx['data'   ] = chart_processed.prop2_values
        chart_ctx['title'  ] = chart_processed.description
    elif chart_processed.type == ChartTypes.POLAR:
        tmpl_js = 'js_polar.html' 
        chart_ctx['labels' ] = chart_processed.prop1_values
        chart_ctx['data'   ] = chart_processed.prop2_values
        chart_ctx['title'  ] = chart_processed.description
    elif chart_processed.type == ChartTypes.GAUGE:
        tmpl_js = 'js_gauge.html' 
        chart_ctx['labels'] = [ chart_processed.prop1_values[0] ]
        val   = chart_processed.prop2_values[0]
        total = sum( chart_processed.prop2_values )  
        chart_ctx['data'  ] = [ int( (val * 100) / total ) ]
    elif chart_processed.type == ChartTypes.GAUGE_STROKED:
        tmpl_js = 'js_gauge_stroked.html' 
        chart_ctx['labels'] = [ chart_processed.prop1_values[0] ]
        val   = chart_processed.prop2_values[0]
        total = sum( chart_processed.prop2_values )  
        chart_ctx['data'  ] = [ int( (val * 100) / total ) ]
    else:
        return HttpResponse( ' > Unsupported type: ' + chart_processed.type )
    
    chart_html = Template( file_load( os.path.join( 'templates', 'includes', 'charts', 'container.html' )) )
    chart_js   = Template( file_load( os.path.join( 'templates', 'includes', 'charts',  tmpl_js )) )

    context['chart_html'] = chart_html.render( Context(chart_ctx ) )
    context['chart_js'  ] = chart_js.render( Context(chart_ctx ) )
            
    return render(request, 'pages/dynamic-charts-embed.html', context)


def get_model_field_names(model, field_type):
    """Returns a list of field names based on the given field type."""
    return [
        field.name for field in model._meta.get_fields() 
        if isinstance(field, field_type)
    ]

def model_charts(request, aPath):

    context = {} 
    user = get_user('test')

    chart_id = request.GET.get('chart_id')
    chart_selected = chart_by_id( chart_id ) 
    chart_template = None 

    if chart_selected:
        print( ' > Selected: ' + str( chart_selected.id ) ) 
        chart_processed = process_chart( chart_selected )        

        chart_ctx  = { }
        chart_ctx['chart' ] = chart_processed

        tmpl_js = None 
        if chart_processed.type == ChartTypes.BAR:
            tmpl_js = 'js_bar.html' 
            chart_ctx['chart_js_title' ] = chart_processed.description
            chart_ctx['chart_js_label' ] = chart_processed.prop2_label
            chart_ctx['chart_js_x' ] = chart_processed.prop1_values
            chart_ctx['chart_js_y' ] = chart_processed.prop2_values
        elif chart_processed.type == ChartTypes.LINE:
            tmpl_js = 'js_line.html'
            chart_ctx['chart_js_title' ] = chart_processed.description
            chart_ctx['chart_js_label' ] = chart_processed.prop2_label
            chart_ctx['chart_js_x' ] = chart_processed.prop1_values
            chart_ctx['chart_js_y' ] = chart_processed.prop2_values
        elif chart_processed.type == ChartTypes.AREA: # NOT_DONE
            tmpl_js = 'js_area.html'
            chart_ctx['chart_title' ] = chart_processed.description
            chart_ctx['labels'   ] = chart_processed.prop1_values
            chart_ctx['data'     ] = chart_processed.prop2_values
        elif chart_processed.type == ChartTypes.COLUMN:
            tmpl_js = 'js_column.html' 
            '''
             'data_series': {'2024-09-01': {'Canada': 0, 'Germany': 0, 'USA': 1},
                 '2024-09-03': {'Canada': 1, 'Germany': 0, 'USA': 0},
                 '2024-09-05': {'Canada': 0, 'Germany': 1, 'USA': 1},
                 '2024-09-06': {'Canada': 0, 'Germany': 0, 'USA': 1}}}
            '''
            data_series = chart_processed.data_series
            chart_ctx['x_data'] = list( data_series.keys() )
            data_series_processed = {}

            # Insert empty lists
            for k in data_series.keys():
                for j in data_series[k].keys():
                    data_series_processed[ j ] = []

            # Insert data in lists
            for k in data_series.keys():
                for j in data_series[k].keys():
                    data_series_processed[ j ].append(data_series[k][j]) 

            chart_ctx['data_series'  ] = data_series_processed

        elif chart_processed.type == ChartTypes.PIE:
            tmpl_js = 'js_pie.html' 
            chart_ctx['chart_js_labels'] = chart_processed.prop1_values
            chart_ctx['chart_js_data'  ] = chart_processed.prop2_values
        elif chart_processed.type == ChartTypes.DONUT:
            tmpl_js = 'js_donut.html' 
            chart_ctx['chart_js_labels'] = chart_processed.prop1_values
            chart_ctx['chart_js_data'  ] = chart_processed.prop2_values
        elif chart_processed.type == ChartTypes.RADIAL:
            tmpl_js = 'js_radial.html' 
            chart_ctx['labels'   ] = chart_processed.prop1_values
            chart_ctx['data'     ] = chart_processed.prop2_values
            chart_ctx['data_sum' ] = sum( chart_processed.prop2_values )
        elif chart_processed.type == ChartTypes.RADAR:
            tmpl_js = 'js_radar.html' 
            chart_ctx['labels' ] = chart_processed.prop1_values
            chart_ctx['data'   ] = chart_processed.prop2_values
            chart_ctx['title'  ] = chart_processed.description
        elif chart_processed.type == ChartTypes.POLAR:
            tmpl_js = 'js_polar.html' 
            chart_ctx['labels' ] = chart_processed.prop1_values
            chart_ctx['data'   ] = chart_processed.prop2_values
            chart_ctx['title'  ] = chart_processed.description
        elif chart_processed.type == ChartTypes.GAUGE:
            tmpl_js = 'js_gauge.html' 
            chart_ctx['labels'] = [ chart_processed.prop1_values[0] ]
            val   = chart_processed.prop2_values[0]
            total = sum( chart_processed.prop2_values )  
            chart_ctx['data'  ] = [ int( (val * 100) / total ) ]
        elif chart_processed.type == ChartTypes.GAUGE_STROKED:
            tmpl_js = 'js_gauge_stroked.html' 
            chart_ctx['labels'] = [ chart_processed.prop1_values[0] ]
            val   = chart_processed.prop2_values[0]
            total = sum( chart_processed.prop2_values )  
            chart_ctx['data'  ] = [ int( (val * 100) / total ) ]
        else:
            return HttpResponse( ' > Unsupported type: ' + chart_processed.type )
        
        chart_html = Template( file_load( os.path.join( 'templates', 'includes', 'charts', 'container.html' )) )
        chart_js   = Template( file_load( os.path.join( 'templates', 'includes', 'charts',  tmpl_js )) )

        context['chart_html'] = chart_html.render( Context(chart_ctx ) )
        context['chart_js'  ] = chart_js.render( Context(chart_ctx ) )

    aModelName  = None
    aModelClass = None

    if aPath in settings.DYNAMIC_CHARTS.keys():
        aModelName  = settings.DYNAMIC_CHARTS[aPath]
        aModelClass = name_to_class(aModelName)

    if not aModelClass:
        return HttpResponse( ' > ERR: Getting ModelClass for path: ' + aPath )
    
    fields = list ( get_model_fields_v( aModelClass ).keys() )
    
    model_series = {}
    idx = 0
    for f in fields:

        f_values = list(aModelClass.objects.values_list(f, flat=True))  # This gives you a list of values for the field
        model_series[f] = [str(i) for i in f_values]

    #print(' > LEN: ' + str( len(model_series) ) )

    transposed_values = list(zip_longest(*model_series.values()))

    transposed_values = transposed_values[0:11]

    charts = [] 
    
    for c in ChartsConfig.objects.filter(user=user, model_name=aModelName):
        charts.append( process_chart( c ) )     

    integer_fields = get_model_field_names(aModelClass, models.IntegerField)
    date_time_fields = get_model_field_names(aModelClass, models.DateTimeField)
    email_fields = get_model_field_names(aModelClass, models.EmailField)
    text_fields = get_model_field_names(aModelClass, (models.TextField, models.CharField))

    read_only_fields = ('id', )
    db_fields = [field.name for field in aModelClass._meta.fields]
    fk_fields = get_model_fk_values(aModelClass)

    form = ChartConfigForm(initial={'model_name': aModelName})

    context['page_title'    ]       = 'Dynamic Charts - ' + aPath.lower().title()
    context[ 'routes'       ]       = settings.DYNAMIC_CHARTS.keys()
    context[ 'link'         ]       = aPath
    context[ 'fields'         ]     = fields
    context[ 'model_name'   ]       = aModelName
    context[ 'model_fields' ]       = list ( get_model_fields_v( aModelClass ).keys() )
    context[ 'model_series' ]       = model_series
    context[ 'model_charts' ]       = charts
    context[ 'read_only_fields' ]   = read_only_fields
    context[ 'transposed_values' ]  = transposed_values
    context[ 'integer_fields' ]     = integer_fields
    context[ 'date_time_fields' ]   = date_time_fields
    context[ 'email_fields' ]       = email_fields
    context[ 'text_fields' ]        = text_fields
    context[ 'fk_fields_keys' ]     = list( fk_fields.keys() )
    context[ 'fk_fields' ]          = fk_fields
    context[ 'db_field_names' ]     = db_fields
    context[ 'form' ]               = form

    return render(request, 'pages/dynamic-charts-model.html', context)


def add_chart(request):
    if request.method == 'POST':

        aModelName  = request.POST['model_name']
        aModelClass = name_to_class( aModelName )

        print( ' > POST model  : ' + aModelName )
        print( ' > model_class : ' + str( aModelClass )  )

        form = ChartConfigForm(request.POST)
        if form.is_valid():
            chart = form.save(commit=False)
            #chart.model = aModelName
            chart.user = request.user
            chart.save()
            print( ' > CHART Created: ' + str( chart.id ) )
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            print( ' > FORM not valid: [' + str( form.errors) + '] [' + str( form.non_field_errors ) + ']' )
    
    return redirect(request.META.get('HTTP_REFERER'))


def delete_chart(request):

    context = {} 
    #user = get_user('test')

    chart_id = request.GET.get('chart_id')
    chart = chart_by_id( chart_id ) 

    if chart:
        chart.delete()

    return redirect(request.META.get('HTTP_REFERER'))