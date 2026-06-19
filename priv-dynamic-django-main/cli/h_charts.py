# -*- encoding: utf-8 -*-
"""
Copyright (c) AppSeed.us
"""

import random, string, json
from datetime import datetime

from django.db import models
from django.core import serializers
from collections import Counter
import statistics

from .common        import *
from .h_util        import *
from .h_code_parser import *
from .h_django      import *

# Django needs to be imported 
apps = get_django()

from home.models import * 
from django_dyn_charts.models import * 

def get_charts_user(aUser):
    return list( ChartsConfig.objects.filter(user=aUser) )

def get_charts_model(aModel):
    return list( ChartsConfig.objects.filter(model=aModel) )

def chart_by_id(aId):
    return ChartsConfig.objects.filter(id=aId).first()

def chart_first():
    return ChartsConfig.objects.all().first()

def chart_last():
    return ChartsConfig.objects.all().last()

def process_chart( aChart ):

    if not aChart:
        return None 
    
    if aChart.type == ChartTypes.BAR:
        return process_chart_bar( aChart )
    elif aChart.type == ChartTypes.LINE:
        return process_chart_line( aChart )
    elif aChart.type == ChartTypes.AREA:
        return process_chart_area( aChart )
    elif aChart.type == ChartTypes.COLUMN:
        return process_chart_column( aChart )
    elif aChart.type == ChartTypes.PIE:
        return process_chart_pie( aChart )
    elif aChart.type == ChartTypes.DONUT:
        return process_chart_donut( aChart )
    elif aChart.type == ChartTypes.RADIAL:
        return process_chart_radial( aChart )
    elif aChart.type == ChartTypes.RADAR:
        return process_chart_radar( aChart )
    elif aChart.type == ChartTypes.POLAR:
        return process_chart_polar( aChart )
    elif aChart.type == ChartTypes.GAUGE:
        return process_chart_gauge( aChart )
    elif aChart.type == ChartTypes.GAUGE_STROKED:
        return process_chart_gauge_stroked( aChart )
    else:
        print( ' > ERR: Unsupported type ['+str(aChart.type)+'] for chart [ID='+str(aChart.id)+' ]' )
        return None 

def extract_filters( aRawFilters ):

    if not aRawFilters:
        return None 
    
    filters = {}

    for f in aRawFilters.split('|'):
        data = f.split('=')
        try:
            filters[ data[0] ] = data[1] 
        except:
            filters[ data[0] ] = ''

    return filters

def apply_filter(aValues, aVerb, aValue):

    retVal  = None 
    applied = False 

    if isinstance(aValues, list):

        retVal = []
        for i in aValues:
            if 'date_format' == aVerb:
                applied = True
                retVal.append( i.strftime('%Y-%m-%d') )
            else:
                # keep input intact, nothing done
                retVal = aValues      

    #print(' > FILTER: <' + aVerb + '>, applied=' + str(applied).upper() )
    #print('     | - INPUT: ' + str( aValues ) )
    #print('     | - OUPUT: ' + str( retVal  ) )

    return retVal

def get_related_props(aDict, aCurrentFilter):

    try:
        suffix = aCurrentFilter.split('_')[0]
        return aDict[suffix], aDict[suffix + '_label'], aDict[suffix + '_q'], aDict[suffix + '_values']
    except:
        return None 

def process_chart_bar( aChartObject ):

    user = aChartObject.user
    
    model = aChartObject.model_name
    type = aChartObject.type
    description = aChartObject.description

    aModelClass = name_to_class(model)
    
    if not aModelClass:
    
        aChartObject.__dict__[ 'prop1_values' ] = []
        aChartObject.__dict__[ 'prop2_values' ] = []

        aChartObject.status  = COMMON.INPUT_ERR
        aChartObject.errInfo = 'Model not found: ' + model

        return aChartObject
    
    try:

        # Post-process data
        # on x, we need distinct values 
        aChartObject.__dict__[ 'prop1_values' ] = list ( aModelClass.objects.values_list( aChartObject.prop1, flat=True) )
        aChartObject.__dict__[ 'prop2_values' ] = [1] * len( aChartObject.__dict__[ 'prop1_values' ] )

        if aChartObject.prop2:
            aChartObject.__dict__[ 'prop2_values' ] = list ( aModelClass.objects.values_list( aChartObject.prop2, flat=True) )
        
        # we can have here count .. etc
        elif aChartObject.prop2_q.lower() in COMMON.CHART_VERBS:
            if COMMON.CHART_VERB_COUNT == aChartObject.prop2_q.lower():
                pass

            # Here is exit point    
            else:
                raise Exception(f"Unsupported verb [{aChartObject.prop2_q}] for property [{aChartObject.prop2}]" )
        else:
            raise Exception(f"Malformed prop_2 [{aChartObject.prop2}] for object" )    

        prop1_values = []
        prop2_values = []

        idx = -1
        for prop1_val in aChartObject.__dict__[ 'prop1_values' ]:
            idx += 1
            prop2_val = aChartObject.__dict__[ 'prop2_values' ][idx]
            print ( ' > ' + str(prop1_val) + ' -> ' + str( prop2_val ) )

            if prop1_val not in prop1_values:
                prop1_values.append( prop1_val )
                prop2_values.append( prop2_val )
            else:
                key_idx = prop1_values.index( prop1_val )
                prop2_values[ key_idx ] += prop2_val 

        aChartObject.__dict__[ 'prop1_values' ] = prop1_values
        aChartObject.__dict__[ 'prop2_values' ] = prop2_values

        return aChartObject
        
    except Exception as e:
        aChartObject.__dict__[ 'prop1_values' ] = []
        aChartObject.__dict__[ 'prop2_values' ] = []

        aChartObject.status  = COMMON.INPUT_ERR
        aChartObject.errInfo = 'ERR: ' + str( e )

        return aChartObject

# https://apexcharts.com/javascript-chart-demos/line-charts/basic/    
def process_chart_line( aChartObject ):

    user = aChartObject.user
    
    model = aChartObject.model_name
    type = aChartObject.type
    description = aChartObject.description

    aModelClass = name_to_class(model)

    for attr, value in aChartObject.__dict__.items():

        if '_filters' not in attr:
            continue

        attr_key_prop   = attr.replace('_filters', '')
        attr_key_q      = attr.replace('_filters', '_q')
        attr_key_values = attr.replace('_filters', '_values')

        prop_name = aChartObject.__dict__[ attr_key_prop ]
        if not prop_name:
            #print ( ' > ATTR [' + attr_key_prop + '] NOT USED' )
            continue 

        prop_q = aChartObject.__dict__[ attr_key_q ]     
        if not prop_q:
            continue

        print ( ' > ATTR [' + prop_name + '] -> [' + prop_q + ']' )
        
        prop_values = list ( aModelClass.objects.values_list( prop_name, flat=True) )

        # Generic processing here
        filters = extract_filters(value)

        if filters:
            print ( '    |-- FILTERS: ' + str( list ( filters.keys() ) ) )
            for verb in filters.keys():
                value = filters[verb]
                prop_values = apply_filter(prop_values, verb, value)
        else:
            print ( '    |-- no filters ')

        print ( '    |-- values: ' + str(prop_values) )    
        aChartObject.__dict__[ attr_key_values ] = prop_values

    # Post-process data
    # on x, we need distinct values 
    prop1_values = []
    prop2_values = []

    idx = -1
    for prop1_val in aChartObject.__dict__[ 'prop1_values' ]:
        idx += 1
        prop2_val = aChartObject.__dict__[ 'prop2_values' ][idx]
        #print ( ' > ' + str(prop1_val) + ' -> ' + str( prop2_val ) )

        if prop1_val not in prop1_values:
            prop1_values.append( prop1_val )
            prop2_values.append( prop2_val )
        else:
            key_idx = prop1_values.index( prop1_val )
            prop2_values[ key_idx ] += prop2_val 

    aChartObject.__dict__[ 'prop1_values' ] = prop1_values
    aChartObject.__dict__[ 'prop2_values' ] = prop2_values

    return aChartObject
    
# https://apexcharts.com/javascript-chart-demos/area-charts/basic/   
def process_chart_area( aChartObject ):

    user = aChartObject.user
    
    model = aChartObject.model_name
    type = aChartObject.type
    description = aChartObject.description

    aModelClass = name_to_class(model)

    for attr, value in aChartObject.__dict__.items():

        if '_filters' not in attr:
            continue

        attr_key_prop   = attr.replace('_filters', '')
        attr_key_q      = attr.replace('_filters', '_q')
        attr_key_values = attr.replace('_filters', '_values')

        prop_name = aChartObject.__dict__[ attr_key_prop ]
        if not prop_name:
            #print ( ' > ATTR [' + attr_key_prop + '] NOT USED' )
            continue 

        prop_q = aChartObject.__dict__[ attr_key_q ]     
        if not prop_q:
            continue

        print ( ' > ATTR [' + prop_name + '] -> [' + prop_q + ']' )
        
        prop_values = list ( aModelClass.objects.values_list( prop_name, flat=True) )

        # Generic processing here
        filters = extract_filters(value)

        if filters:
            print ( '    |-- FILTERS: ' + str( list ( filters.keys() ) ) )
            for verb in filters.keys():
                value = filters[verb]
                prop_values = apply_filter(prop_values, verb, value)
        else:
            print ( '    |-- no filters ')

        print ( '    |-- values: ' + str(prop_values) )    
        aChartObject.__dict__[ attr_key_values ] = prop_values

    # Post-process data
    # on x, we need distinct values 
    prop1_values = []
    prop2_values = []

    idx = -1
    for prop1_val in aChartObject.__dict__[ 'prop1_values' ]:
        idx += 1
        prop2_val = aChartObject.__dict__[ 'prop2_values' ][idx]
        #print ( ' > ' + str(prop1_val) + ' -> ' + str( prop2_val ) )

        if prop1_val not in prop1_values:
            prop1_values.append( prop1_val )
            prop2_values.append( prop2_val )
        else:
            key_idx = prop1_values.index( prop1_val )
            prop2_values[ key_idx ] += prop2_val 

    aChartObject.__dict__[ 'prop1_values' ] = prop1_values
    aChartObject.__dict__[ 'prop2_values' ] = prop2_values

    return aChartObject

# https://apexcharts.com/javascript-chart-demos/column-charts/basic/  
def process_chart_column( aChartObject ):

    user = aChartObject.user
    
    model = aChartObject.model_name
    type = aChartObject.type
    description = aChartObject.description

    aModelClass = name_to_class(model)

    for attr, value in aChartObject.__dict__.items():

        if '_filters' not in attr:
            continue

        attr_key_prop   = attr.replace('_filters', '')
        attr_key_q      = attr.replace('_filters', '_q')
        attr_key_values = attr.replace('_filters', '_values')

        prop_name = aChartObject.__dict__[ attr_key_prop ]
        if not prop_name:
            #print ( ' > ATTR [' + attr_key_prop + '] NOT USED' )
            continue 

        prop_q = aChartObject.__dict__[ attr_key_q ]     
        if not prop_q:
            continue

        print ( ' > ATTR [' + prop_name + '] -> [' + prop_q + ']' )
        
        prop_values = list ( aModelClass.objects.values_list( prop_name, flat=True) )

        # Generic processing here
        filters = extract_filters(value)

        if filters:
            print ( '    |-- FILTERS: ' + str( list ( filters.keys() ) ) )
            for verb in filters.keys():
                value = filters[verb]
                prop_values = apply_filter(prop_values, verb, value)
        else:
            print ( '    |-- no filters ')

        print ( '    |-- values: ' + str(prop_values) )    
        aChartObject.__dict__[ attr_key_values ] = prop_values

    print( ' >  aChartObject.PROP1_values : ' + str( aChartObject.prop1_values ) )
    print( ' >  aChartObject.PROP2_values : ' + str( aChartObject.prop2_values ) )

    # aChartObject.PROP1_values : ['2024-09-01', '2024-09-03', '2024-09-05', '2024-09-05', '2024-09-06']
    # aChartObject.PROP2_values : ['USA', 'Canada', 'Germany', 'USA', 'USA']

    # Post-process data
    # on x, we need distinct values 
    prop1_values          = aChartObject.prop1_values
    prop1_values_distinct = []
    for v in prop1_values:
        if v not in prop1_values_distinct:
            prop1_values_distinct.append( v ) 
    prop2_values          = aChartObject.prop2_values
    prop2_values_distinct = list( set(prop2_values) )
    data_series          = {} # attached series 

    print( ' >  aChartObject.PROP1_distinct : ' + str( prop1_values_distinct ) )
    print( ' >  aChartObject.PROP2_distinct : ' + str( prop2_values_distinct ) )

    # Build data_series
    for p in prop1_values_distinct:
        data_series[p] = {}
        for v in prop2_values_distinct:
            data_series[p][v] = 0

    pp( data_series  )

    idx = -1
    for prop1_val in aChartObject.__dict__[ 'prop1_values' ]:
        idx += 1
        prop2_val = aChartObject.__dict__[ 'prop2_values' ][idx]
        #print( '['+str(idx)+'] ' + prop1_val + ', ' +  prop2_val ) 
        data_series[prop1_val][prop2_val] += 1

    #pp( data_series  )

    aChartObject.__dict__[ 'prop1_values' ] = prop1_values
    aChartObject.__dict__[ 'prop2_values' ] = prop2_values
    aChartObject.__dict__[ 'data_series'  ] = data_series

    return aChartObject

# https://apexcharts.com/javascript-chart-demos/pie-charts/simple-pie-chart/
def process_chart_pie( aChartObject ):

    user = aChartObject.user
    model = aChartObject.model_name
    type = aChartObject.type
    description = aChartObject.description

    aModelClass = name_to_class(model)

    for attr, value in aChartObject.__dict__.items():

        if '_filters' not in attr:
            continue

        attr_key_prop   = attr.replace('_filters', '')
        attr_key_q      = attr.replace('_filters', '_q')
        attr_key_values = attr.replace('_filters', '_values')

        prop_name = aChartObject.__dict__[ attr_key_prop ]
        if not prop_name:
            #print ( ' > ATTR [' + attr_key_prop + '] NOT USED' )
            continue 

        prop_q = aChartObject.__dict__[ attr_key_q ]     
        if not prop_q:
            continue

        print ( ' > ATTR [' + prop_name + '] -> [' + prop_q + ']' )
        
        prop_values = list ( aModelClass.objects.values_list( prop_name, flat=True) )

        # Generic processing here
        filters = extract_filters(value)

        if filters:
            print ( '    |-- FILTERS: ' + str( list ( filters.keys() ) ) )
            for verb in filters.keys():
                value = filters[verb]
                prop_values = apply_filter(prop_values, verb, value)
        else:
            print ( '    |-- no filters ')

        print ( '    |-- values: ' + str(prop_values) )    
        aChartObject.__dict__[ attr_key_values ] = prop_values

    # Post-process data
    # on x, we need distinct values 
    prop1_values = []
    prop2_values = []

    # Y-axis might be null
    if not aChartObject.__dict__[ 'prop2_values' ]:
        aChartObject.__dict__[ 'prop2' ] = 'Count'
        aChartObject.__dict__[ 'prop2_values' ] = [1] * len( aChartObject.__dict__[ 'prop1_values' ] )

    idx = -1
    for prop1_val in aChartObject.__dict__[ 'prop1_values' ]:
        idx += 1
                
        prop2_val = aChartObject.__dict__[ 'prop2_values' ][idx]
        #print ( ' > ' + str(prop1_val) + ' -> ' + str( prop2_val ) )

        if prop1_val not in prop1_values:
            prop1_values.append( prop1_val )
            prop2_values.append( prop2_val )
        else:
            key_idx = prop1_values.index( prop1_val )
            prop2_values[ key_idx ] += prop2_val 

    aChartObject.__dict__[ 'prop1_values' ] = prop1_values
    aChartObject.__dict__[ 'prop2_values' ] = prop2_values

    return aChartObject

# https://apexcharts.com/javascript-chart-demos/pie-charts/simple-donut/
def process_chart_donut( aChartObject ):

    user = aChartObject.user
    
    model = aChartObject.model_name
    type = aChartObject.type
    description = aChartObject.description

    aModelClass = name_to_class(model)

    for attr, value in aChartObject.__dict__.items():

        if '_filters' not in attr:
            continue

        attr_key_prop   = attr.replace('_filters', '')
        attr_key_q      = attr.replace('_filters', '_q')
        attr_key_values = attr.replace('_filters', '_values')

        prop_name = aChartObject.__dict__[ attr_key_prop ]
        if not prop_name:
            #print ( ' > ATTR [' + attr_key_prop + '] NOT USED' )
            continue 

        prop_q = aChartObject.__dict__[ attr_key_q ]     
        if not prop_q:
            continue

        print ( ' > ATTR [' + prop_name + '] -> [' + prop_q + ']' )
        
        prop_values = list ( aModelClass.objects.values_list( prop_name, flat=True) )

        # Generic processing here
        filters = extract_filters(value)

        if filters:
            print ( '    |-- FILTERS: ' + str( list ( filters.keys() ) ) )
            for verb in filters.keys():
                value = filters[verb]
                prop_values = apply_filter(prop_values, verb, value)
        else:
            print ( '    |-- no filters ')

        print ( '    |-- values: ' + str(prop_values) )    
        aChartObject.__dict__[ attr_key_values ] = prop_values

    # Post-process data
    # on x, we need distinct values 
    prop1_values = []
    prop2_values = []

    idx = -1
    for prop1_val in aChartObject.__dict__[ 'prop1_values' ]:
        idx += 1
        prop2_val = aChartObject.__dict__[ 'prop2_values' ][idx]
        #print ( ' > ' + str(prop1_val) + ' -> ' + str( prop2_val ) )

        if prop1_val not in prop1_values:
            prop1_values.append( prop1_val )
            prop2_values.append( prop2_val )
        else:
            key_idx = prop1_values.index( prop1_val )
            prop2_values[ key_idx ] += prop2_val 

    aChartObject.__dict__[ 'prop1_values' ] = prop1_values
    aChartObject.__dict__[ 'prop2_values' ] = prop2_values

    return aChartObject

# https://apexcharts.com/javascript-chart-demos/radialbar-charts/multiple-radialbars/
def process_chart_radial( aChartObject ):

    user = aChartObject.user
    
    model = aChartObject.model_name
    type = aChartObject.type
    description = aChartObject.description

    aModelClass = name_to_class(model)

    for attr, value in aChartObject.__dict__.items():

        if '_filters' not in attr:
            continue

        attr_key_prop   = attr.replace('_filters', '')
        attr_key_q      = attr.replace('_filters', '_q')
        attr_key_values = attr.replace('_filters', '_values')

        prop_name = aChartObject.__dict__[ attr_key_prop ]
        if not prop_name:
            #print ( ' > ATTR [' + attr_key_prop + '] NOT USED' )
            continue 

        prop_q = aChartObject.__dict__[ attr_key_q ]     
        if not prop_q:
            continue

        print ( ' > ATTR [' + prop_name + '] -> [' + prop_q + ']' )
        
        prop_values = list ( aModelClass.objects.values_list( prop_name, flat=True) )

        # Generic processing here
        filters = extract_filters(value)

        if filters:
            print ( '    |-- FILTERS: ' + str( list ( filters.keys() ) ) )
            for verb in filters.keys():
                value = filters[verb]
                prop_values = apply_filter(prop_values, verb, value)
        else:
            print ( '    |-- no filters ')

        print ( '    |-- values: ' + str(prop_values) )    
        aChartObject.__dict__[ attr_key_values ] = prop_values

    # Post-process data
    # on x, we need distinct values 
    prop1_values = []
    prop2_values = []

    idx = -1
    for prop1_val in aChartObject.__dict__[ 'prop1_values' ]:
        idx += 1
        prop2_val = aChartObject.__dict__[ 'prop2_values' ][idx]
        #print ( ' > ' + str(prop1_val) + ' -> ' + str( prop2_val ) )

        if prop1_val not in prop1_values:
            prop1_values.append( prop1_val )
            prop2_values.append( prop2_val )
        else:
            key_idx = prop1_values.index( prop1_val )
            prop2_values[ key_idx ] += prop2_val 

    aChartObject.__dict__[ 'prop1_values' ] = prop1_values
    aChartObject.__dict__[ 'prop2_values' ] = prop2_values

    return aChartObject

# https://apexcharts.com/javascript-chart-demos/radar-charts/basic/
def process_chart_radar( aChartObject ):

    user = aChartObject.user
    
    model = aChartObject.model_name
    type = aChartObject.type
    description = aChartObject.description

    aModelClass = name_to_class(model)

    for attr, value in aChartObject.__dict__.items():

        if '_filters' not in attr:
            continue

        attr_key_prop   = attr.replace('_filters', '')
        attr_key_q      = attr.replace('_filters', '_q')
        attr_key_values = attr.replace('_filters', '_values')

        prop_name = aChartObject.__dict__[ attr_key_prop ]
        if not prop_name:
            #print ( ' > ATTR [' + attr_key_prop + '] NOT USED' )
            continue 

        prop_q = aChartObject.__dict__[ attr_key_q ]     
        if not prop_q:
            continue

        print ( ' > ATTR [' + prop_name + '] -> [' + prop_q + ']' )
        
        prop_values = list ( aModelClass.objects.values_list( prop_name, flat=True) )

        # Generic processing here
        filters = extract_filters(value)

        if filters:
            print ( '    |-- FILTERS: ' + str( list ( filters.keys() ) ) )
            for verb in filters.keys():
                value = filters[verb]
                prop_values = apply_filter(prop_values, verb, value)
        else:
            print ( '    |-- no filters ')

        print ( '    |-- values: ' + str(prop_values) )    
        aChartObject.__dict__[ attr_key_values ] = prop_values

    # Post-process data
    # on x, we need distinct values 
    prop1_values = []
    prop2_values = []

    idx = -1
    for prop1_val in aChartObject.__dict__[ 'prop1_values' ]:
        idx += 1
        prop2_val = aChartObject.__dict__[ 'prop2_values' ][idx]
        #print ( ' > ' + str(prop1_val) + ' -> ' + str( prop2_val ) )

        if prop1_val not in prop1_values:
            prop1_values.append( prop1_val )
            prop2_values.append( prop2_val )
        else:
            key_idx = prop1_values.index( prop1_val )
            prop2_values[ key_idx ] += prop2_val 

    aChartObject.__dict__[ 'prop1_values' ] = prop1_values
    aChartObject.__dict__[ 'prop2_values' ] = prop2_values

    return aChartObject

# https://apexcharts.com/javascript-chart-demos/polar-area-charts/basic/
def process_chart_polar( aChartObject ):

    user = aChartObject.user
    
    model = aChartObject.model_name
    type = aChartObject.type
    description = aChartObject.description

    aModelClass = name_to_class(model)

    for attr, value in aChartObject.__dict__.items():

        if '_filters' not in attr:
            continue

        attr_key_prop   = attr.replace('_filters', '')
        attr_key_q      = attr.replace('_filters', '_q')
        attr_key_values = attr.replace('_filters', '_values')

        prop_name = aChartObject.__dict__[ attr_key_prop ]
        if not prop_name:
            #print ( ' > ATTR [' + attr_key_prop + '] NOT USED' )
            continue 

        prop_q = aChartObject.__dict__[ attr_key_q ]     
        if not prop_q:
            continue

        print ( ' > ATTR [' + prop_name + '] -> [' + prop_q + ']' )
        
        prop_values = list ( aModelClass.objects.values_list( prop_name, flat=True) )

        # Generic processing here
        filters = extract_filters(value)

        if filters:
            print ( '    |-- FILTERS: ' + str( list ( filters.keys() ) ) )
            for verb in filters.keys():
                value = filters[verb]
                prop_values = apply_filter(prop_values, verb, value)
        else:
            print ( '    |-- no filters ')

        print ( '    |-- values: ' + str(prop_values) )    
        aChartObject.__dict__[ attr_key_values ] = prop_values

    # Post-process data
    # on x, we need distinct values 
    prop1_values = []
    prop2_values = []

    idx = -1
    for prop1_val in aChartObject.__dict__[ 'prop1_values' ]:
        idx += 1
        prop2_val = aChartObject.__dict__[ 'prop2_values' ][idx]
        #print ( ' > ' + str(prop1_val) + ' -> ' + str( prop2_val ) )

        if prop1_val not in prop1_values:
            prop1_values.append( prop1_val )
            prop2_values.append( prop2_val )
        else:
            key_idx = prop1_values.index( prop1_val )
            prop2_values[ key_idx ] += prop2_val 

    aChartObject.__dict__[ 'prop1_values' ] = prop1_values
    aChartObject.__dict__[ 'prop2_values' ] = prop2_values

    return aChartObject

# https://apexcharts.com/javascript-chart-demos/radialbar-charts/semi-circle-gauge/
def process_chart_gauge( aChartObject ):

    user = aChartObject.user
    
    model = aChartObject.model_name
    type = aChartObject.type
    description = aChartObject.description

    aModelClass = name_to_class(model)

    for attr, value in aChartObject.__dict__.items():

        if '_filters' not in attr:
            continue

        attr_key_prop   = attr.replace('_filters', '')
        attr_key_q      = attr.replace('_filters', '_q')
        attr_key_values = attr.replace('_filters', '_values')

        prop_name = aChartObject.__dict__[ attr_key_prop ]
        if not prop_name:
            #print ( ' > ATTR [' + attr_key_prop + '] NOT USED' )
            continue 

        prop_q = aChartObject.__dict__[ attr_key_q ]     
        if not prop_q:
            continue

        print ( ' > ATTR [' + prop_name + '] -> [' + prop_q + ']' )
        
        prop_values = list ( aModelClass.objects.values_list( prop_name, flat=True) )

        # Generic processing here
        filters = extract_filters(value)

        if filters:
            print ( '    |-- FILTERS: ' + str( list ( filters.keys() ) ) )
            for verb in filters.keys():
                value = filters[verb]
                prop_values = apply_filter(prop_values, verb, value)
        else:
            print ( '    |-- no filters ')

        print ( '    |-- values: ' + str(prop_values) )    
        aChartObject.__dict__[ attr_key_values ] = prop_values

    # Post-process data
    # on x, we need distinct values 
    prop1_values = []
    prop2_values = []

    idx = -1
    for prop1_val in aChartObject.__dict__[ 'prop1_values' ]:
        idx += 1
        prop2_val = aChartObject.__dict__[ 'prop2_values' ][idx]
        #print ( ' > ' + str(prop1_val) + ' -> ' + str( prop2_val ) )

        if prop1_val not in prop1_values:
            prop1_values.append( prop1_val )
            prop2_values.append( prop2_val )
        else:
            key_idx = prop1_values.index( prop1_val )
            prop2_values[ key_idx ] += prop2_val 

    aChartObject.__dict__[ 'prop1_values' ] = prop1_values
    aChartObject.__dict__[ 'prop2_values' ] = prop2_values

    return aChartObject

# https://apexcharts.com/javascript-chart-demos/radialbar-charts/stroked-gauge/
def process_chart_gauge_stroked( aChartObject ):

    user = aChartObject.user
    
    model = aChartObject.model_name
    type = aChartObject.type
    description = aChartObject.description

    aModelClass = name_to_class(model)

    for attr, value in aChartObject.__dict__.items():

        if '_filters' not in attr:
            continue

        attr_key_prop   = attr.replace('_filters', '')
        attr_key_q      = attr.replace('_filters', '_q')
        attr_key_values = attr.replace('_filters', '_values')

        prop_name = aChartObject.__dict__[ attr_key_prop ]
        if not prop_name:
            #print ( ' > ATTR [' + attr_key_prop + '] NOT USED' )
            continue 

        prop_q = aChartObject.__dict__[ attr_key_q ]     
        if not prop_q:
            continue

        print ( ' > ATTR [' + prop_name + '] -> [' + prop_q + ']' )
        
        prop_values = list ( aModelClass.objects.values_list( prop_name, flat=True) )

        # Generic processing here
        filters = extract_filters(value)

        if filters:
            print ( '    |-- FILTERS: ' + str( list ( filters.keys() ) ) )
            for verb in filters.keys():
                value = filters[verb]
                prop_values = apply_filter(prop_values, verb, value)
        else:
            print ( '    |-- no filters ')

        print ( '    |-- values: ' + str(prop_values) )    
        aChartObject.__dict__[ attr_key_values ] = prop_values

    # Post-process data
    # on x, we need distinct values 
    prop1_values = []
    prop2_values = []

    idx = -1
    for prop1_val in aChartObject.__dict__[ 'prop1_values' ]:
        idx += 1
        prop2_val = aChartObject.__dict__[ 'prop2_values' ][idx]
        #print ( ' > ' + str(prop1_val) + ' -> ' + str( prop2_val ) )

        if prop1_val not in prop1_values:
            prop1_values.append( prop1_val )
            prop2_values.append( prop2_val )
        else:
            key_idx = prop1_values.index( prop1_val )
            prop2_values[ key_idx ] += prop2_val 

    aChartObject.__dict__[ 'prop1_values' ] = prop1_values
    aChartObject.__dict__[ 'prop2_values' ] = prop2_values

    return aChartObject

def suggest_charts(model_class, sample_size=100):
    field_types = {}
    for field in model_class._meta.fields:
        field_types[field.name] = field.get_internal_type()

    numeric_fields = [name for name, type in field_types.items() if type in ['IntegerField', 'FloatField', 'DecimalField']]
    categorical_fields = [name for name, type in field_types.items() if type in ['CharField', 'TextField', 'BooleanField']]
    date_fields = [name for name, type in field_types.items() if type in ['DateField', 'DateTimeField']]

    # Fetch sample data
    sample_data = model_class.objects.all()[:sample_size]

    suggestions = []

    # Suggest bar charts for categorical fields
    for field in categorical_fields:
        values = [getattr(obj, field) for obj in sample_data]
        unique_values = set(values)
        if len(unique_values) <= 10:  # Limit to fields with 10 or fewer unique values
            suggestions.append({
                "chart_type": "bar",
                "title": f"Distribution of {field}",
                "x_axis": field,
                "y_axis": "Count"
            })

    # Suggest line charts for date fields with numeric fields
    for date_field in date_fields:
        for numeric_field in numeric_fields:
            suggestions.append({
                "chart_type": "line",
                "title": f"{numeric_field} over {date_field}",
                "x_axis": date_field,
                "y_axis": numeric_field
            })

    # Suggest scatter plots for pairs of numeric fields
    if len(numeric_fields) >= 2:
        for i in range(len(numeric_fields)):
            for j in range(i+1, len(numeric_fields)):
                suggestions.append({
                    "chart_type": "scatter",
                    "title": f"{numeric_fields[i]} vs {numeric_fields[j]}",
                    "x_axis": numeric_fields[i],
                    "y_axis": numeric_fields[j]
                })

    # Suggest pie charts for categorical fields with few unique values
    for field in categorical_fields:
        values = [getattr(obj, field) for obj in sample_data]
        unique_values = set(values)
        if 2 <= len(unique_values) <= 5:
            suggestions.append({
                "chart_type": "pie",
                "title": f"Distribution of {field}",
                "labels": field,
                "values": "Count"
            })

    return json.dumps({"suggested_charts": suggestions}, indent=2)
	
def suggest_charts_and_analyze(model_class, sample_size=100):
    field_types = {}
    for field in model_class._meta.fields:
        field_types[field.name] = field.get_internal_type()

    numeric_fields = [name for name, type in field_types.items() if type in ['IntegerField', 'FloatField', 'DecimalField']]
    categorical_fields = [name for name, type in field_types.items() if type in ['CharField', 'TextField', 'BooleanField']]
    date_fields = [name for name, type in field_types.items() if type in ['DateField', 'DateTimeField']]

    # Fetch sample data
    sample_data = list(model_class.objects.all()[:sample_size])
    
    suggestions = []
    column_descriptions = {}
    data_summary = []

    # Chart suggestion and data analysis
    for field, field_type in field_types.items():
        values = [getattr(obj, field) for obj in sample_data if getattr(obj, field) is not None]
        
        if field in numeric_fields:
            if values:
                mean = statistics.mean(values)
                median = statistics.median(values)
                data_summary.append(f"The average {field} is {mean:.2f}, with a median of {median:.2f}.")
                column_descriptions[field] = f"Numeric field representing {field}. Values range from {min(values)} to {max(values)}."
            
            suggestions.append({
                "chart_type": "histogram",
                "title": f"Distribution of {field}",
                "x_axis": field,
                "y_axis": "Frequency"
            })

        elif field in categorical_fields:
            value_counts = Counter(values)
            most_common = value_counts.most_common(1)[0] if value_counts else None
            if most_common:
                data_summary.append(f"The most common {field} is '{most_common[0]}', appearing {most_common[1]} times.")
            column_descriptions[field] = f"Categorical field representing {field}. It has {len(value_counts)} unique values."

            if len(value_counts) <= 10:
                suggestions.append({
                    "chart_type": "bar",
                    "title": f"Distribution of {field}",
                    "x_axis": field,
                    "y_axis": "Count"
                })
            if 2 <= len(value_counts) <= 5:
                suggestions.append({
                    "chart_type": "pie",
                    "title": f"Distribution of {field}",
                    "labels": field,
                    "values": "Count"
                })

        elif field in date_fields:
            if values:
                earliest = min(values)
                latest = max(values)
                data_summary.append(f"The {field} ranges from {earliest} to {latest}.")
            column_descriptions[field] = f"Date field representing {field}."

            for numeric_field in numeric_fields:
                suggestions.append({
                    "chart_type": "line",
                    "title": f"{numeric_field} over {field}",
                    "x_axis": field,
                    "y_axis": numeric_field
                })

    # Suggest scatter plots for pairs of numeric fields
    if len(numeric_fields) >= 2:
        for i in range(len(numeric_fields)):
            for j in range(i+1, len(numeric_fields)):
                suggestions.append({
                    "chart_type": "scatter",
                    "title": f"{numeric_fields[i]} vs {numeric_fields[j]}",
                    "x_axis": numeric_fields[i],
                    "y_axis": numeric_fields[j]
                })

    # Generate overall data sentiment
    sentiment = "Neutral"
    if data_summary:
        positive_keywords = ['increase', 'growth', 'improvement', 'higher', 'better']
        negative_keywords = ['decrease', 'decline', 'lower', 'worse', 'poor']
        
        positive_count = sum(1 for keyword in positive_keywords for summary in data_summary if keyword in summary.lower())
        negative_count = sum(1 for keyword in negative_keywords for summary in data_summary if keyword in summary.lower())
        
        if positive_count > negative_count:
            sentiment = "Positive"
        elif negative_count > positive_count:
            sentiment = "Negative"

    # Generate data story
    model_name = model_class.__name__.lower()
    field_names = set(field.lower() for field in field_types.keys())
    
    story = f"This dataset appears to be about {model_name}. "
    
    # Detect common business metrics
    if 'revenue' in field_names or 'sales' in field_names:
        story += "It likely contains information about business performance, possibly tracking sales or revenue. "
    if 'customer' in ' '.join(field_names):
        story += "There seems to be customer-related data, which could be useful for customer relationship management. "
    if 'product' in ' '.join(field_names):
        story += "Product information is present, suggesting this could be an inventory or product performance dataset. "
    if 'date' in ' '.join(field_names) or any(field for field in date_fields):
        story += "The presence of date fields indicates this data is time-based, possibly for trend analysis. "
    if 'location' in field_names or 'country' in field_names or 'city' in field_names:
        story += "Geographic information is included, which could be used for regional analysis. "
    
    # Add information about the nature of the data
    if len(numeric_fields) > len(categorical_fields):
        story += "The data is primarily numeric, which is conducive to quantitative analysis and reporting. "
    else:
        story += "The data has a significant number of categorical fields, which could be useful for segmentation and qualitative analysis. "
    
    # Speculate on potential use cases
    story += f"This {model_name} dataset could potentially be used for "
    use_cases = []
    if 'sales' in model_name or 'revenue' in field_names:
        use_cases.append("sales forecasting")
    if 'customer' in ' '.join(field_names):
        use_cases.append("customer segmentation")
    if 'product' in ' '.join(field_names):
        use_cases.append("product performance analysis")
    if date_fields:
        use_cases.append("trend analysis")
    if 'location' in field_names or 'country' in field_names or 'city' in field_names:
        use_cases.append("geographic market analysis")
    
    if use_cases:
        story += ", ".join(use_cases) + "."
    else:
        story += "various business intelligence purposes."

    result = {
        "suggested_charts": suggestions,
        "data_sentiment": sentiment,
        "data_summary": " ".join(data_summary),
        "column_descriptions": column_descriptions,
        "data_story": story
    }

    return json.dumps(result, indent=2)
