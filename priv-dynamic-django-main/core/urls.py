# -*- encoding: utf-8 -*-
"""
Copyright (c) AppSeed.us
"""

from django.contrib import admin
from django.urls import path, include, re_path 
from rest_framework.authtoken.views import obtain_auth_token
from django.conf import settings
from django.views.generic.base import TemplateView
from django.contrib.sitemaps.views import sitemap
from django.views.static import serve

urlpatterns = [
    path("", include("home.urls")),
    path("admin/", admin.site.urls),
    path("", include("django_dyn_api.urls")),
    path("", include("django_dyn_dt.urls")),
    path("", include("django_dyn_charts.urls")),
    # path("", include("admin_berry.urls")),
    path('', include('admin_berry_pro.urls')),
    path("login/jwt/", view=obtain_auth_token),
    path("__debug__/", include("debug_toolbar.urls")),

    re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}), 
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),   

    path(
        "sitemap.xml",
        TemplateView.as_view(template_name="sitemap.xml", content_type="text/xml"),
    ), 
    path(
        "robots.txt",
        TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),
    ),    
]
