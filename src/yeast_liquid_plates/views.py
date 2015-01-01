import colorsys
import sys, traceback, os, multiprocessing, logging, json, csv, datetime, time

# from django.db import connection

from django import db
# import db_config #the import automatically initiates db check if it can be less frequent

from django.shortcuts import render_to_response
from django.template import RequestContext
# from django.http import HttpResponseRedirect
# from django.core.urlresolvers import reverse
# from django.shortcuts import render
# 
# from http.client import HTTPResponse
from django.http.response import HttpResponse
from lab import settings
from yeast_libraries.models import YeastPlate_Model, YeastLibrary_Model



from yeast_liquid_plates.spectrometer_data_reader import SpectrometerDataReader
from yeast_liquid_plates.models import SpectrometerExperiment_Model,\
    ParseDataProcess_Model, SpectrometerWellData_Model, LiquidYeastPlate_Model

from yeast_liquid_plates.model_helper import LiquidExperimentHelper


import numpy as np
import pandas as pd

from bokeh.resources import CDN
from bokeh.embed import file_html, components

from bokeh.plotting import figure

from lab_util.util import pr


# Create your views here.
def liquid_plate_analysis(request):
    """
    """
    
#     print('liquid_plate_analysis(): ')
#     print('')
#     
#     g = request.GET
#     print(g)
    
    return render_to_response(
            'yeast_liquid_plates/liquid_plate_analysis.html',
            {},
            context_instance=RequestContext(request)
        )



def get_available_liquid_plates(request):
    """
    """
    
    r = ['baffle']
    
    try:
         
        r = os.listdir(path = os.path.join(settings.LIQUID_PLATE_ROOT, 'data'))
        
    except Exception: 
            
        print('exception: ', sys.exc_info)
        traceback.print_exc()
        
        
    for d in r:
        
        if d.startswith('.'):
            
            r.remove(d)
     
        
    return HttpResponse(json.dumps(r))


def get_raw_data_file(request):
    """
    """
    g = request.GET
    
    plate = g.__getitem__('plate')
#     print('plate: ', plate)
    r = ['baffle']
    
    try:
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="Stam.csv"'
        
        writer = csv.writer(response)
        
        writer.writerow(['Column', 'Row', 'Is Empty', 'Area Scaled', 'Ratio', 'Center X', 'Center Y'])
    
        return response
#         os.path.join(settings.LIQUID_PLATE_ROOT, 'data', )
        
    except Exception: 
            
        print('exception: ', sys.exc_info)
        traceback.print_exc()
     
        
    return HttpResponse(json.dumps(r))


def affiliate_data_to_plate(request):
    """
    """
    print('')
    print('affiliate_data_to_plate: ')
    print('')
    
    try:
        g = request.GET
        plate_data_dir = g.__getitem__('plate_data_dir')

        print('plate_data_dir: ', plate_data_dir)
        
        experiments = SpectrometerExperiment_Model.objects.filter(data_dir_name = plate_data_dir)
        

        if experiments.count() > 0:
            
            print('There exists an experiment linked to the directory')
            return HttpResponse(json.dumps({'status': 'error', 'message': plate_data_dir + ' directory is already affiliated with a plate'}))
        
        
        plate_pk = int(g.__getitem__('plate_pk'))
        print('plate_pk: ', plate_pk)
        
        path = os.path.join(settings.LIQUID_PLATE_ROOT, 'data', plate_data_dir)
        
        liquid_plate = LiquidYeastPlate_Model.objects.get(pk = plate_pk)
        
        
        
        plate_id = liquid_plate.pk
        format_id = liquid_plate.yeast_plate.scheme.format.pk
        
        s = SpectrometerDataReader()
        
        process_status, created = ParseDataProcess_Model.objects.get_or_create(dir_path = path)
        
        process_table_name = process_status._meta.db_table
        print('process_status._meta.db_table: ', process_table_name) 
        
        if created:
        
            process_status.status = 'bussy'
            process_status.save()
        
        elif process_status.status == 'bussy':
            
            print('an old process is bussy returning')
            return HttpResponse('still bussy')
            
        elif process_status.status == 'failed':
            
            print('an old process has failed retrying')
            process_status.status = 'bussy'
            process_status.save()
        
        process = multiprocessing.Process(target=SpectrometerDataReader.getData, args=(s, settings.DB_NAME, path, plate_id, format_id, process_status.pk, process_table_name))
        process.start()
        
        r = {'process_pk' : process_status.pk}
        
        return HttpResponse(json.dumps(r))
#         affiliateData(settings.DB_NAME, path, format_id)
    
    except Exception: 
            
        print('exception: ', sys.exc_info)
        traceback.print_exc()

    
    return HttpResponse('scaramoo')



def affiliate_follow_up(request):
    """
    """
    
    g = request.GET
    
    try:
    
        process_pk = g.__getitem__('process_pk')
    #     print('process_pk:', process_pk)
        
        process = ParseDataProcess_Model.objects.get(pk=process_pk)
        
        status = process.status
        
        print('in affiliate_follow_up   snapshot_process.status:', status)
            
        r = {}
        r['status'] = status
        r['process_pk'] = process_pk
        
        if status == 'complete':
            
            e = process.experiment
#             
#             e = SpectrometerExperiment_Model.objects.get(pk=experiment_pk)
            rr = {}
            rr[e.plate.yeast_plate.stack.pk] = {'name': e.__str__(), 'id': e.pk, 'copy_id': e.plate.yeast_plate.stack.pk}
            r['experiment'] = rr
            
    except Exception: 
            
        print('exception: ', sys.exc_info)
        traceback.print_exc()


    
    return HttpResponse(json.dumps(r))



def get_spectrometer_experiments(request):
    """
    """
    g = request.GET
    
    user = g.__getitem__('user')
    print('user: ', user)
    
    helper = LiquidExperimentHelper()
    
    r = helper.byUserLibs(user)
    
    
    print('get_spectrometer_experiments: ', r)
     
        
    return HttpResponse(json.dumps(r))




def get_spectrometer_experiments_by_plate(request):
    """
    """
    g = request.GET
    
    plate_pk = g.__getitem__('plate_pk')
    print('plate_pk: ', plate_pk)
    
    r = []
    
        
    try:
        
        experiments = SpectrometerExperiment_Model.objects.filter(plate__pk = plate_pk)    
        
        for e in experiments:
            
            r.append({'name': e.__str__(), 'id': e.pk, 'plate_id': e.plate.yeast_plate.pk})
    
    except Exception: 
        
        print('exception: ', sys.exc_info)
        traceback.print_exc()   
    
    
    rr = {plate_pk : r}
    
    print('get_spectrometer_experiments_by_plate: ', rr)
     
        
    return HttpResponse(json.dumps(rr))



def growth_graph(request):
    
    if request.is_ajax():
        if request.method == 'POST':
            print ('Raw Data:', request.body) 
            
            print ('type(request.body):', type(request.body)) 
            
            try:
            
                j = json.loads(request.body.decode("utf-8"))
            
                print(j)
            
            except Exception: 
                
                print('exception: ', sys.exc_info)
                traceback.print_exc()   
                
    experiment_pk =  j['id']         
    
    
    samples = SpectrometerWellData_Model.objects.filter(sample__experiment__pk = experiment_pk, row = 3, column = 4)
    
    for sample in samples:
        
        print('str(sample.getStdev()):  ', str(sample.getStdev()))
    

    
    return HttpResponse("BO OK")


def growth_graphs(request):
    
    if request.is_ajax():
        if request.method == 'POST':
#             print ('Raw Data:', request.body) 
            
#             print ('type(request.body):', type(request.body)) 
            
            try:

                figure1 = figure(
                    tools=["pan", "resize", "wheel_zoom", "box_zoom", "reset", "save", "hover"],
                    title="Spectrometer Growth Rates",
                    background_fill="#EFFFFF",
                    # x_axis_type="datetime",
                    x_axis_label = "Time",
                    y_axis_label = "Stdv Growth"
                )

                # figure1.ygrid.grid_line_color = 8
                # figure1.ygrid.grid_line_width = 9
                # figure1.axis.major_label_text_font_size = 8
                # figure1.axis.major_label_text_font_style = 8
                figure1.axis.major_label_standoff = 15       # distance of tick labels from ticks
                # figure1.axis.axis_line_color =       8             # color, or None, to suppress the line
                # figure1.xaxis.major_label_orientation =     8      # radians, "horizontal", "vertical", "normal"
                # figure1.xaxis.major_tick_in = 80         # distance ticks extends into the plot
                # figure1.xaxis.major_tick_out = 10       # and distance they extend out
                # figure1.xaxis.major_tick_line_color = 8

            
                d_wells = json.loads(request.body.decode("utf-8"))
                print(d_wells)

                line_metas = {}
                copy_ranges = divideRange(0, 1, len(d_wells.items()))

                i = 0

                for key, value in d_wells.items() :

                    if len(value.items()) == 0:
                        pr('An empty copy value has been sent wasted color range')
                        continue

                    plate_ranges = divideRange(copy_ranges[i][0], copy_ranges[i][1], len(value.items()))

                    line_metas[key] = {}

                    i = i + 1
                    j = 0

                    for key1, value1 in value.items():

                        if len(value1.items()) == 0:
                            pr('An empty plate value has been sent wasted color range')
                            continue

                        line_metas[key][key1] = {}

                        line_colors = rangeToColors(plate_ranges[j], len(value1.items()))

                        j = j + 1
                        k = 0

                        for key2, value2 in value1.items():
    #                         print ('     key2: ', key2, '  value1: ', value1)

                            line_metas[key][key1][key2] = {}

                            color = line_colors[k]
                            k = k + 1

                            row, column = value2
                            print ('     row: ', row, '  column: ', column)
                            print('')

                            # TODO make sure the right experiment is chosen to avoid combining data
                            well_data = SpectrometerWellData_Model.objects.filter(sample__experiment__plate__yeast_plate__pk = int(key1), row = row, column = column).order_by("sample__end_time")


                            if len(well_data) == 0:

                                line_metas[key][key1]['comment'] = 'No experiment connected'
                                pr('No experiment connected')
                                continue

                            line_metas[key][key1][key2]['name'] = row + column + ' ' + well_data[0].sample.experiment.plate.yeast_plate.full_name()
                            line_metas[key][key1][key2]['color'] = color

                            points = []
                            x = []
                            first = 0

                            for datum in well_data:

                                point = datum.getStdev()
                                print('str(datum.getStdev()):  ', str(point))
                                points.append(point)

                                end_time = time.mktime(datum.sample.end_time.timetuple())


                                # print('schedule: ', end_time)
                                if len(x) == 0:

                                    x.append(0)
                                    first = end_time

                                else:

                                    x.append(end_time - first)


                            # print(str(x))

                            figure1.line(x,points, color=color, tools=[])

                            print('')


                # html = file_html(figure1, CDN, "my plot")

                print(' ')
                print(' ')


                script, div = components(figure1, CDN)

                # print(div)
                # print("")
                # print("scaramoo")
                # print("")
                # print(script)

                r = {}
                r['html'] = script+div
                r['json'] = line_metas

                return HttpResponse(json.dumps(r))

                # return HttpResponse(script+div)

            except Exception:

                print('exception: ', sys.exc_info)
                traceback.print_exc()
                return HttpResponse(json.dumps({'html':'<h1>' + sys.exc_info + '</h1>'}))

    return HttpResponse('<h1>Error at Server</h1>')





def divideRange(begin, end, divisions):

    i = (end - begin)/divisions

    ranges = []

    for x in range(divisions):

        range1 = (x*i, x*i + i)
        ranges.append(range1)

    return ranges


def rangeToColors(range1, divisions):

    i = (range1[0] - range1[1])/divisions

    colors = []

    for x in range(divisions):

        hue = x*i + i/2
        rgb = colorsys.hsv_to_rgb(hue, 0.5, 0.7)

        pr(str(rgb))


        color = rgb_to_hex1(rgb)

        # color = color.replace('-', '')
        #
        colors.append(color)

    print('colors: ', colors)

    return colors





def colorRanges(n=5):

    pr('str(n):  ' + str(n))
    HSV_tuples = [(x*1.0/n, 0.5, 0.5) for x in range(n)]
    RGB_tuples = map(lambda x: colorsys.hsv_to_rgb(*x), HSV_tuples)

    print('type(RGB_tuples): ', type(RGB_tuples))

    return RGB_tuples



def colorRanges1(n=5):

    pr('str(n):  ' + str(n))
    HSV_tuples = [(x*1.0/n, 0.5, 0.5) for x in range(n)]
    RGB_tuples = map(lambda x: colorsys.hsv_to_rgb(*x), HSV_tuples)

    return RGB_tuples


def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

def rgb_to_hex(rgb):

    print(type(rgb))

    return '#%02x%02x%02x' % rgb


def rgb_to_hex1(rgb):

    rgb1 = []

    for x in rgb:
        rgb1.append(x*255)

    return '#%02x%02x%02x' % tuple(rgb1)




def stam():

    # print(hex_to_rgb("#ffffff"))             #==> (255, 255, 255)
    # print(hex_to_rgb("#ffffffffffff"))       #==> (65535, 65535, 65535)
    # print(rgb_to_hex((255, 255, 255)))       #==> '#ffffff'
    # print(rgb_to_hex((65535, 65535, 65535))) #==> '#ffffffffffff'

    print('yo: ', rgb_to_hex1((1, 1, 1)))