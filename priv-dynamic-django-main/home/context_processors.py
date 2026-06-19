from django.conf import settings

def get_settings(request):
    return {'settings': settings}

def analytics_key(request):
    return {
        'GOOGLE_ANALYTICS_KEY': getattr(settings, 'GOOGLE_ANALYTICS_KEY', 'NOT_SET'),
    }
