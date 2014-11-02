
# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

urlpatterns = patterns('yeast_libraries.views',
    url(r'^library_creator/$', 'library_creator', name='library_creator'),
    url(r'^library_copier/$', 'library_copier', name='library_copier'),
    url(r'^stack_register/$', 'stack_register', name='stack_register'),
    url(r'^stack_register_gui/$', 'stack_register_gui', name='stack_register_gui'),
    url(r'^snapshot_model_map/$', 'snapshot_model_map', name='snapshot_model_map'),
    url(r'^plate_map/$', 'plate_map', name='plate_map'),
    
    url(r'^snapshot_map/$', 'snapshot_map', name='snapshot_map'),
    url(r'^copy_snapshot_map/$', 'copy_snapshot_map', name='copy_snapshot_map'),
    url(r'^lib_stack_map/$', 'lib_stack_map', name='lib_stack_map'),
    url(r'^snapshot/$', 'snapshot', name='snapshot'),
    url(r'^snapshot_follow_up/$', 'snapshot_follow_up', name='snapshot_follow_up'),
    url(r'^private_lib_list/$', 'private_lib_list', name='private_lib_list'),
    
    url(r'^getSnapshotAnalysis/$', 'getSnapshotAnalysis', name='getSnapshotAnalysis'),
    url(r'^getBatchSnapshotAnalysis/$', 'getBatchSnapshotAnalysis', name='getBatchSnapshotAnalysis'),

    url(r'^getSnapshotAnalysisHistory/$', 'getSnapshotAnalysisHistory', name='getSnapshotAnalysisHistory'),

    url(r'^getSnapshotOverLibAnalysis/$', 'getSnapshotOverLibAnalysis', name='getSnapshotOverLibAnalysis'),
    url(r'^show_analysis/$', 'show_analysis', name='show_analysis'),
    url(r'^compare_snapshots/$', 'compare_snapshots', name='compare_snapshots'),
    url(r'^compare_copies/$', 'compare_copies', name='compare_copies'),
    
    url(r'^cam/$', 'cam', name='cam'),
    url(r'^simple_snapshot/$', 'simple_snapshot', name='simple_snapshot'),
    url(r'^annoymous_snapshot/$', 'annoymous_snapshot', name='annoymous_snapshot'),
    
    url(r'^get_image/$', 'get_image', name='get_image'),
    url(r'^get_analysis_as_csv/$', 'get_analysis_as_csv', name='get_analysis_as_csv'),
    
    url(r'^mockUp/$', 'mockUp', name='mockUp'),
    
    url(r'^get_plate_pattern/$', 'get_plate_pattern', name='get_plate_pattern'),
)
