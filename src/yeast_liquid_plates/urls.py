
# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

urlpatterns = patterns('yeast_liquid_plates.views',
    url(r'^liquid_plate_analysis/$', 'liquid_plate_analysis', name='liquid_plate_analysis'),
    url(r'^get_available_liquid_plates/$', 'get_available_liquid_plates', name='get_available_liquid_plates'),
    url(r'^get_raw_data_file/$', 'get_raw_data_file', name='get_raw_data_file'),
    url(r'^affiliate_data_to_plate/$', 'affiliate_data_to_plate', name='affiliate_data_to_plate'),
    url(r'^affiliate_follow_up/$', 'affiliate_follow_up', name='affiliate_follow_up'),
    url(r'^get_spectrometer_experiments/$', 'get_spectrometer_experiments', name='get_spectrometer_experiments'),
    url(r'^get_spectrometer_experiments_by_plate/$', 'get_spectrometer_experiments_by_plate', name='get_spectrometer_experiments_by_plate'),
    url(r'^growth_graph/$', 'growth_graph', name='growth_graph'),
    url(r'^growth_graphs/$', 'growth_graphs', name='growth_graphs'),
)



