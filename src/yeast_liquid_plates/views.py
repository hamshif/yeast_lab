import sys, traceback, os, multiprocessing, logging, json, csv, datetime

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
            
                j = json.loads(request.body.decode("utf-8"))
            
                print(j)
                
                for key, value in j.items() :
#                     print ('key: ', key, '  value: ', value)
                    
                    copy_pk, plate_pk = key.split('p')
                    print ('copy_pk: ', copy_pk, '  plate_pk: ', plate_pk)
                    
                    for key1, value1 in value.items() :
#                         print ('     key1: ', key1, '  value1: ', value1)
                    
                        row, column = value1
                        print ('     row: ', row, '  column: ', column)
                
            
            except Exception: 
                
                print('exception: ', sys.exc_info)
                traceback.print_exc()   
                
#     experiment_pk =  j['id']         
#     
#     
#     
#     samples = SpectrometerWellData_Model.objects.filter(sample__experiment__pk = experiment_pk, row = 3, column = 4)
#     
#     for sample in samples:
#         
#         print('str(sample.getStdev()):  ', str(sample.getStdev()))
    
    print('boom chakalaka')
    
    return HttpResponse(json.dumps({"": "BO OK"}))
