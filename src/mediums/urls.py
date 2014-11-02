# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

urlpatterns = patterns('mediums.views',
    url(r'^medium_creator/$', 'medium_creator', name='medium_creator'),
)