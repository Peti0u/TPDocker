from django.db import models
from django.contrib.auth.models import User

class ChartTypes(models.TextChoices):
	BAR             = 'BAR', 'Bar'
	LINE            = 'LINE', 'Line'
	AREA            = 'AREA', 'Area'
	COLUMN          = 'COLUMN', 'Column'
	PIE             = 'PIE', 'Pie'
	DONUT           = 'DONUT', 'Donut'
	RADIAL          = 'RADIAL', 'Radial'
	RADAR           = 'RADAR', 'Radar'
	POLAR           = 'POLAR', 'Polar'
	GAUGE           = 'GAUGE', 'Gauge'
	GAUGE_STROKED   = 'GAUGE_STROKED', 'Gauge_Stroked'

class QualityTypes(models.TextChoices):
	X_AXIS          = 'x-axis', 'x-axis'
	Y_AXIS          = 'y-axis', 'y-axis'
	VERB_SUM        = 'sum', 'sum'
	VERB_COUNT      = 'count', 'count'
	VERB_AVG        = 'avg', 'avg'
	VERB_MIN        = 'min', 'min'
	VERB_MAX        = 'max', 'max'

class FilterTypes(models.TextChoices):
	DATE_FORMAT     = 'date_format', 'date_format'
	UPPERCASE       = 'upercase', 'upercase'
	LOWERCASE       = 'lowercase', 'lowercase'

class ChartsConfig(models.Model):

    user            = models.ForeignKey(User, on_delete=models.CASCADE)
    model_name      = models.CharField(max_length=255)

    title           = models.CharField(max_length=128,null=True, blank=True)
    type            = models.CharField(max_length=50, choices=ChartTypes.choices)
    description     = models.TextField(null=True, blank=True)

    status          = models.IntegerField(default=-1)
    errInfo         = models.CharField(max_length=250,null=True,blank=True)
                                       
    prop1           = models.CharField(max_length=50,null=True, blank=True)
    prop1_label     = models.CharField(max_length=50,null=True, blank=True)
    prop1_q         = models.CharField(max_length=50,null=True, blank=True, choices=QualityTypes.choices, default=QualityTypes.X_AXIS)
    prop1_filters   = models.CharField(max_length=128,null=True, blank=True, choices=FilterTypes.choices)
    prop1_values    = models.CharField(max_length=512,null=True, blank=True)

    prop2           = models.CharField(max_length=50,null=True, blank=True)
    prop2_label     = models.CharField(max_length=50,null=True, blank=True)
    prop2_q         = models.CharField(max_length=50,null=True, blank=True, choices=QualityTypes.choices, default=QualityTypes.Y_AXIS)
    prop2_filters   = models.CharField(max_length=128,null=True, blank=True, choices=FilterTypes.choices)
    prop2_values    = models.CharField(max_length=512,null=True, blank=True)

    '''
    prop3           = models.CharField(max_length=50,null=True, blank=True)
    prop3_label     = models.CharField(max_length=50,null=True, blank=True)
    prop3_q         = models.CharField(max_length=50,null=True, blank=True, choices=QualityTypes.choices)
    prop3_filters   = models.CharField(max_length=128,null=True, blank=True, choices=FilterTypes.choices)
    prop3_values    = models.CharField(max_length=512,null=True, blank=True)

    prop4           = models.CharField(max_length=50,null=True, blank=True)
    prop4_label     = models.CharField(max_length=50,null=True, blank=True)
    prop4_q         = models.CharField(max_length=50,null=True, blank=True, choices=QualityTypes.choices)
    prop4_filters   = models.CharField(max_length=128,null=True, blank=True, choices=FilterTypes.choices)
    prop4_values    = models.CharField(max_length=512,null=True, blank=True)

    prop5           = models.CharField(max_length=50,null=True, blank=True)
    prop5_label     = models.CharField(max_length=50,null=True, blank=True)
    prop5_q         = models.CharField(max_length=50,null=True, blank=True, choices=QualityTypes.choices)
    prop5_filters   = models.CharField(max_length=128,null=True, blank=True, choices=FilterTypes.choices)
    prop5_values    = models.CharField(max_length=512,null=True, blank=True)

    prop6           = models.CharField(max_length=50,null=True, blank=True)
    prop6_label     = models.CharField(max_length=50,null=True, blank=True)
    prop6_q         = models.CharField(max_length=50,null=True, blank=True, choices=QualityTypes.choices)
    prop6_filters   = models.CharField(max_length=128,null=True, blank=True, choices=FilterTypes.choices)
    prop6_values    = models.CharField(max_length=512,null=True, blank=True)
    '''