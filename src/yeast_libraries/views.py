import sys, traceback, os, multiprocessing, logging, json, csv


from django.views.decorators.csrf import csrf_protect
# from django import db
# import db_config #the import automatically initiates db check if it can be less frequent

from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
# from django.http import HttpResponseRedirect
# from django.core.urlresolvers import reverse
# from django.shortcuts import render
# 
# from http.client import HTTPResponse
from django.http.response import HttpResponse
from django.views.decorators.cache import never_cache

from yeast_libraries.models import StorageLocation_Model,\
    YeastLibrary_Model, YeastPlateStack_Model, YeastPlate_Model,\
    SnapshotBatch_Model, PlateSnapshot_Model, SnapshotProcess_Model,\
    PlateScheme_Model, LocusAnalysis_Model, PlateLocus_Model, YeastStrain_Model
from mediums.models import Batch_Model

from datetime import datetime

from cmd_utils.cam import PlateCam

# from image_analysis.image_processor import ImageAnalysisControler

from excels.lib_parser import LibraryParser
from yeast_libraries import views_util

from lab import settings
from lab_util.util import pr, numberToLetterASCII

from cmd_utils.exiv2 import Exiv2
from yeast_libraries import views_util
from yeast_liquid_plates.models import LiquidYeastPlate_Model


from yeast_libraries.model_helper import LibraryHelper, CopyHelper, PlateHelper, SnapshotBatchHelper



grid = 'smoken'

multiprocessing.log_to_stderr(logging.DEBUG)


def mockUp(request):

    return render_to_response(
            'yeast_libraries/mockUp.html',
            {},
            context_instance=RequestContext(request)
        )


def compare_copies(request):
    
    print('compare_copies()')
    
    try:
    
        g = request.GET
        
        copy_pk = g.__getitem__('copy_pk')
        print('copy_pk:', copy_pk)
        
        copy_pk2 = g.__getitem__('copy_pk2')
        print('copy_pk2:', copy_pk2)

        batch_index = int(g.__getitem__('batch_index')) + 1
        print('batch_index:', str(batch_index))
        
        batch2_index = int(g.__getitem__('batch2_index')) + 1
        print('batch2_index:', str(batch2_index))
        
        get_excel = g.__getitem__('get_excel')
        print('get_excel:', get_excel)
        
        print('type(batch_index): ', type(batch_index))
        
        
        snapshots = PlateSnapshot_Model.objects.filter(batch__plate__stack__pk = copy_pk, batch__index = batch_index).order_by('batch__plate__scheme__index')
        
        comp_snapshots = PlateSnapshot_Model.objects.filter(batch__plate__stack__pk = copy_pk2, batch__index = batch2_index).order_by('batch__plate__scheme__index')
        
        len1 = len(snapshots)
        len2 = len(comp_snapshots)
        
        print('len1:', len1)
        print('len2:', len2)
        
        all_compared = []
        plate_names = []
        comp_plate_names = []
        
        for i in range(len1):
         
            if i >= len2:
                break
             
            snapshot = snapshots[i]
            comp_snapshot = comp_snapshots[i]
             
            if snapshot.batch.plate.scheme.index == comp_snapshot.batch.plate.scheme.index:
             
                format = snapshot.batch.plate.scheme.format
 
                analysis1 = analysis(format, snapshot)
                 
                compared_analysis = analysis(format, comp_snapshot)
                 
                compared = analysis1
             
                for i in range(len(analysis1)):
                     
                    for j in range(len(analysis1[i])):
                     
                        if analysis1[i][j] ==  compared_analysis[i][j]:
                             
                            compared[i][j] = 'ok'
                     
                        else:
                             
                            compared[i][j] = 'discrepant'
                             
                all_compared.append(compared)
                plate_names.append(snapshot.batch.plate.full_str())
                comp_plate_names.append(comp_snapshot.batch.plate.full_str())
                 
            else:
                print('TODO deal with different plate indexes')
                    
    except Exception:
        print('exception: ', sys.exc_info)
        traceback.print_exc()
        
        return HttpResponse('durum boom') 
    
    
    if get_excel == 'false':
        
        return HttpResponse(json.dumps(all_compared))
    else:
        
        response = HttpResponse(content_type='text/csv')

        filename = snapshots[0].batch.plate.stack.__str__() + ' compared to ' + comp_snapshots[0].batch.plate.stack.__str__()

        response['Content-Disposition'] = 'attachment; filename="' + filename + '.csv"'
        
        writer = csv.writer(response)
        
        for i in range(len(all_compared)):
            
            compared = all_compared[i]

            writer.writerow(['', '', '', '', 'Comparison'])
            writer.writerow([''])
            writer.writerow([plate_names[i]])
            writer.writerow([comp_plate_names[i]])
            writer.writerow([''])
            writer.writerow([''])
            
            for compared_row in compared:
        
                writer.writerow(compared_row)
                
            writer.writerow([''])
            writer.writerow([''])
    
        return response 



def compare_snapshots(request):
    
    #print(request)
    
#     print('QUERY_STRING:  ')
#     print(request.META['QUERY_STRING'])
    
    try:
    
        g = request.GET
        
        plate_pk = g.__getitem__('plate_pk')
#         print('plate_pk:', plate_pk)
        
        snapshot_pk = g.__getitem__('snapshot_pk')
#         print('snapshot_pk:', snapshot_pk)
        
        compared_plate_pk = g.__getitem__('compared_plate_pk')
#         print('compared_plate_pk:', compared_plate_pk)
        
        compared_snapshot_pk = g.__getitem__('compared_snapshot_pk')
#         print('compared_snapshot_pk:', compared_snapshot_pk)
        
        get_excel = g.__getitem__('get_excel')
#         print('get_excel:', get_excel)
    

        
        plate = YeastPlate_Model.objects.get(pk = plate_pk)
        format = plate.scheme.format
        snapshot = PlateSnapshot_Model.objects.get(pk = snapshot_pk)
        
        analysis1 = analysis(format, snapshot)
        
        
        compared_plate = YeastPlate_Model.objects.get(pk = compared_plate_pk)
        compared_format = compared_plate.scheme.format
        compared_snapshot = PlateSnapshot_Model.objects.get(pk = compared_snapshot_pk)
        
        compared_analysis = analysis(compared_format, compared_snapshot)
        
        compared = analysis1
    
        for i in range(len(analysis1)):
            
            for j in range(len(analysis1[i])):
            
                if analysis1[i][j] ==  compared_analysis[i][j]:
                    
                    compared[i][j] = 0
            
                else:
                    
                    compared[i][j] = 1
                    
    except Exception:
        print('exception: ', sys.exc_info)
        traceback.print_exc()
        
        return HttpResponse('durum boom') 
    
    
    if get_excel == 'false':
        
        return HttpResponse(json.dumps(compared))
    else:
        
        response = HttpResponse(content_type='text/csv')

        filename = plate.full_str() + ' compared to ' + compared_plate.full_str()

        response['Content-Disposition'] = 'attachment; filename="' + filename + '.csv"'
        
        writer = csv.writer(response)
        
        writer.writerow(['', '', '', '', 'Comparison'])
        writer.writerow([''])
        writer.writerow([plate.full_str()])
        writer.writerow([compared_plate.full_str()])
        writer.writerow([''])
        writer.writerow([''])
        
        for compared_row in compared:
    
            writer.writerow(compared_row)
    
        return response
            

        # writer.writerow([''])
        # writer.writerow([''])
        #
        #
        # for compared_row in compared:
        #
        #     i = 0
        #     translated_row = []
        #
        #     for c in compared_row:
        #
        #         if c == 0:
        #
        #             translated_row.append('  ok')
        #
        #         else:
        #
        #             translated_row.append('discrepant')
        #
        #         i = i+1
        #
        #     writer.writerow(translated_row)

        return response


def getSnapshotAnalysis(request):
    """
    """
    g = request.GET
    
    
    try:
    
        snapshot_pk = int(g.__getitem__('snapshot_pk'))
#         print('snapshot_pk:', snapshot_pk)
        
        lib_pk = int(g.__getitem__('lib_pk'))
#         print('lib_pk:', lib_pk)
        
        get_excel = g.__getitem__('get_excel')
#         print('get_excel:', get_excel)
        
    except Exception: 
           
        print('exception: ', sys.exc_info)
        traceback.print_exc()

    
    try:
        
        library = YeastLibrary_Model.objects.get(pk = lib_pk)
        snapshot = PlateSnapshot_Model.objects.get(pk = snapshot_pk)
        plate = snapshot.batch.plate
        
        plate_scheme = plate.scheme
        
        format = plate_scheme.format
        
        snapshot_analysis = analysis(format, snapshot)
        
            
        if get_excel == 'false':
        
            return HttpResponse(json.dumps(snapshot_analysis))
        
        else:

            filename = plate.stack.__str__() + '_' +snapshot.__str__()+'.csv'

            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="' + filename + '"'
            
            writer = csv.writer(response)
            writer.writerow([])
            writer.writerow([filename])
            writer.writerow([])
            
            for locus in snapshot_analysis:
        
#                 print(locus)
                writer.writerow(locus)
#                 writer.writerow(', '.join(locus))
                
            writer.writerow([])    
            
            writer.writerow(['Column', 'Row', 'Is Empty', 'Area Scaled', 'Ratio', 'Center X', 'Center Y', 'Strain'])
        
        
            full = fullLibAnalysis(format, snapshot)
            
            for locus in full:
                
                writer.writerow(locus)
                
                
            return response
    

            
            return HttpResponse(str(grid))  
    except Exception: 
           
        print('exception: ', sys.exc_info)
        traceback.print_exc()
     
        
    return HttpResponse('baffle')



def getSnapshotAnalysisHistory(request):
    """
    """
    g = request.GET
    
    
    try:
        snapshot_pk = int(g.__getitem__('snapshot_pk'))
        print('snapshot_pk:', snapshot_pk)
        
        get_excel = g.__getitem__('get_excel')
        print('get_excel:', get_excel)
    
        
    except Exception: 
           
        print('exception: ', sys.exc_info)
        traceback.print_exc()

    
    try:
        
        snapshot = PlateSnapshot_Model.objects.get(pk = snapshot_pk)
        copy = snapshot.batch.plate.stack

        plates = YeastPlate_Model.objects.filter(stack=copy).order_by('scheme__index')

        snapshots = []

        for plate in plates:

            snapshots1 = PlateSnapshot_Model.objects.filter(batch__plate = plate)
            snapshots.extend(snapshots1)


        pr(copy.__str__())


            
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="' + copy.__str__() + '.csv"'

        writer = csv.writer(response)

        for snapshot in snapshots:

            snapshotAnalysisHistory(snapshot, writer)

        return response

    except Exception: 
           
        print('exception: ', sys.exc_info)
        traceback.print_exc()
     
        
    return HttpResponse('baffle')





def snapshotAnalysisHistory(snapshot, writer):
    """
    """

    plate_index = snapshot.batch.plate.scheme.index
    copy = snapshot.batch.plate.stack
    library = copy.library

    pr(copy.__str__())

    snapshots = [snapshot]

    while True:

        if copy.parent:

            copy = copy.parent
        else:
            break

        # this should be a get it's quick and dirty fix for double lib info from a migration script

        snapshot = PlateSnapshot_Model.objects.filter(batch__plate__stack = copy, batch__plate__scheme__index = plate_index, batch__index = 1)

        for s in snapshot:

            print('snapshot.__str__():   ', s.__str__(), '  ', s.image_path)


        if(len(snapshot)>0):

            snapshot = snapshot[0]

        else:
            continue

        print('')
        snapshots.append(snapshot)


    print('len(snapshots): ', len(snapshots))

    # writer.writerow(['Discrepancy report for plates of ' + copy.__str__()])
    # writer.writerow([])
    # writer.writerow([])

    discrepant = {}
    times = []

    for snapshot in snapshots:

        # writer.writerow([snapshot.batch.plate.stack.__str__() ])

        pattern = libPattern(snapshot.batch.plate.scheme)
        format1 = snapshot.batch.plate.scheme.format
        analysis1 = analysis(format1, snapshot)


        for i in range(len(analysis1)):

            for j in range(len(analysis1[i])):

                # print('pat: ', pattern[i][j][0], '  an: ', analysis1[i][j])
                #

                if pattern[i][j][0] != analysis1[i][j]:

                    m = 'The colony is occupying a location which should be vacant'

                    discrepancy_type = "contamin"

                    if pattern[i][j][0] == 0:

                        m = 'The original library colony is gone'

                        discrepancy_type = "extinct"

                    t1 = snapshot.batch.plate.stack.time_stamp

                    if not snapshot.batch.plate.stack.time_stamp in times:

                        times.append(t1)


                    key = str(i+1) + "_" + str(j+1)

                    if key in discrepant:
                        discrepant[key][t1] = discrepancy_type
                    else:
                        discrepant[key] = {t1: discrepancy_type}


                    # writer.writerow(['', "row: " + str(i), " column: " + str(j), m])
                    # writer.writerow([])

    print('')
    print('')


    writer.writerow(['Discrepancy history for plate ' + str(plate_index) + ' in ' + library.__str__()])
    writer.writerow([])
    writer.writerow([])

    times.insert(0, '')
    times.insert(0, '')

    writer.writerow(times)

    for k in discrepant.keys():

        r = k.split('_')

        from lab_util.util import numberToLetterASCII
        r[0] = 'row: ' + numberToLetterASCII(int(r[0])-1)
        r[1] = 'col: ' + r[1]

        for t1 in times[2:]:

            if t1 in discrepant[k].keys():

                r.append(discrepant[k][t1])

            else:

                r.append('')

        writer.writerow(r)

    writer.writerow([])
    writer.writerow([])





def getBatchSnapshotAnalysis(request):
    """
    """
    g = request.GET
    
    
    try:
        copy_pk = int(g.__getitem__('copy_pk'))
        print('copy_pk:', copy_pk)
        
        get_excel = g.__getitem__('get_excel')
        print('get_excel:', get_excel)
        
        discrepancy_report = g.__getitem__('discrepancy_report')
        print('discrepancy_report:', discrepancy_report)
        
    except Exception: 
           
        print('exception: ', sys.exc_info)
        traceback.print_exc()

    
    try:
        
        copy = YeastPlateStack_Model.objects.get(pk = copy_pk)
        snapshots = PlateSnapshot_Model.objects.filter(batch__plate__stack__pk = copy_pk).order_by('batch__plate__scheme__index')
        
        print('len(snapshots): ', len(snapshots))
        
            
        if discrepancy_report == 'true':
            
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="'+ copy.__str__() + '.csv"'
            
            writer = csv.writer(response)
            writer.writerow(['Discrepancy report for plates of ' + copy.__str__()]);
            writer.writerow([]);
            writer.writerow([]);
            
            for snapshot in snapshots:
        
                writer.writerow([snapshot.batch.plate.__str__() ])

                scheme = snapshot.batch.plate.scheme
                pattern = libPattern(scheme)
                format1 = snapshot.batch.plate.scheme.format
                analysis1 = analysis(format1, snapshot)
                
                for i in range(len(analysis1)):
    
                    for j in range(len(analysis1[i])):
               
                        if pattern[i][j][0] != analysis1[i][j]:
                        
                            m = 'The colony is occupying a location which should be vacant'
                            
                            
                            if pattern[i][j][0] == 0:
                                
                                m = 'The original library colony is gone'

                            row = numberToLetterASCII(i)
                            column = j+1

                            locus = PlateLocus_Model.objects.filter(scheme = scheme, row = row, column = column)

                            strain = 'empty'

                            if len(locus) > 0:

                                strain = locus[0].strain.name


                            writer.writerow(['', "row: " + row, " column: " + str(column),  'strain: ', strain, '',  m])
                            writer.writerow([])
              
            return response
            
            
            
        
        analyses = []
        
        for snapshot in snapshots:
        
            analysis0 = []
            format1 = snapshot.batch.plate.scheme.format
            
            snapshot_analysis = fullLibAnalysis(format1, snapshot)
            
            analysis0.append(snapshot_analysis)
            
            analyses.append(analysis0)
        
            
            
        if get_excel == 'false':
        
            return HttpResponse(json.dumps(analyses))
        
        else:
            
            print('shakshuka')
            
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="'+ copy.__str__() + '.csv"'
            
            writer = csv.writer(response)
            writer.writerow(['Image analyses for plates of ' + copy.__str__()]);
            writer.writerow([]);
            writer.writerow([]);
            
            i = 0
            
            for snapshot_analysis in analyses:
            
                snapshot = snapshots[i]
                i = i + 1
                writer.writerow([snapshot.__str__()]);
                writer.writerow([]);
                
                writer.writerow(['Column', 'Row', 'Is Empty', 'Area Scaled', 'Ratio', 'Center X', 'Center Y', 'Strain'])
            
                for locus in snapshot_analysis:
            
                    for something in locus:
    #                 print(locus)
                        writer.writerow(something)
#                         writer.writerow(', '.join(locus))
                
                writer.writerow([]);
                writer.writerow([]);
                
                
            return response
    

            
            return HttpResponse(str(grid))  
    except Exception: 
           
        print('exception: ', sys.exc_info)
        traceback.print_exc()
     
        
    return HttpResponse('buffle')




def analysis(format, snapshot):
    
#     print('analysis in views')
    
    print(snapshot.image_path)
    print(snapshot.batch.index)
    
    width = format.width_loci
    length = format.length_loci
    
#     print('width: ', width, 'length: ', length)
    
    snapshot_analysis = []
    
    for i in range(length):
        snapshot_analysis.append(['']*width)
    
    
    analysis = LocusAnalysis_Model.objects.filter(snapshot = snapshot)
    
    
    if len(analysis) >= 1:
            
        for locus in analysis:
    
            if not locus.is_empty:
                
                snapshot_analysis[locus.row][locus.column] = 1
                
            else:
                print('locus is empty')
                    
    else:
        print('no analysis')   
        
        try:
        
        # this is for checking
        
            # processUtil = ImageAnalysisControler()
            
            snapshot_process, created = SnapshotProcess_Model.objects.get_or_create(snapshot_pk=snapshot.pk)
                 
            if created:
                print('snapshot_process.__str__(): ', snapshot_process.__str__(), ' was just created')
                  
            else:
                print('snapshot_process.__str__(): ', snapshot_process.__str__(), ' was just retrieved')
                  
                if snapshot_process.status == 'bussy':
                    print('a former process is probably still working on analyzing the pic')
                
    
            snapshot_process.status = 'bussy'
            snapshot_process.save()   
                
    
            process_pk = snapshot_process.pk
            
            process_table_name = snapshot_process._meta.db_table
#             print('snapshot_process._meta.db_table: ', process_table_name) 
            db_name = settings.DB_NAME
            
            img_full_path = os.path.join(settings.PLATE_IMAGE_ROOT, snapshot.image_path)
            
#             print('img_full_path: ', img_full_path)
            
            
            # process = multiprocessing.Process(target=ImageAnalysisControler.processImage, args=(processUtil, settings.BASE_DIR, settings.PLATE_IMAGE_ROOT, img_full_path, snapshot.pk, process_pk, db_name, process_table_name))
            # process.start()
            
            
        except Exception: 
               
            print('exception: ', sys.exc_info)
            traceback.print_exc()

        
    return snapshot_analysis



def fullLibAnalysis(format, snapshot):
    
#     print('analysis in views')
    
    width = format.width_loci
    length = format.length_loci
    
#     print('width: ', width, 'length: ', length)
    
    snapshot_analysis = []    
    
    analysis = LocusAnalysis_Model.objects.filter(snapshot = snapshot)
    
    if len(analysis) >= 1:
            
        for locus in analysis:

            strain = ''

            if locus.locus:

                if locus.locus.strain:

                    strain = locus.locus.strain


            l = [locus.column, locus.row, locus.is_empty, locus.area_scaled, locus.ratio, locus.center_x, locus.center_y, strain]
            snapshot_analysis.append(l)
        
    return snapshot_analysis



def getSnapshotOverLibAnalysis(request):
    """
    """
#     print('getSnapshotOverLibAnalysis()')
    
    g = request.GET
    
    snapshot_pk = int(g.__getitem__('snapshot_pk'))
#     print('snapshot_pk:', snapshot_pk)
    
    lib_pk = int(g.__getitem__('lib_pk'))
#     print('lib_pk:', lib_pk)

    plate_pk = int(g.__getitem__('plate_pk'))
#     print('plate_pk:', plate_pk)
    
    get_excel = g.__getitem__('get_excel')
#     print('get_excel:', get_excel)
    
    discrepancy = g.__getitem__('discrepancy')
#     print('discrepancy:', discrepancy)
    
    try:
        
        plate = YeastPlate_Model.objects.get(pk = plate_pk)
        plate_scheme = plate.scheme
        
        snapshot_analysis = libPattern(plate_scheme)
        
        snapshot = PlateSnapshot_Model.objects.get(pk = snapshot_pk)
        format = plate_scheme.format
        analysis1 = analysis(format, snapshot)
        

 
        if get_excel == 'false':
            
            for i in range(len(analysis1)):
            
                for j in range(len(analysis1[i])):
                
                    snapshot_analysis[i][j][1] = analysis1[i][j]

            return HttpResponse(json.dumps(snapshot_analysis))
        
        else:
            
            response = HttpResponse(content_type='text/csv')
            filename = 'Copy Analysis Over Library Pattern ' + snapshot.__str__();
            response['Content-Disposition'] = 'attachment; filename="' + filename + '.csv"'
            writer = csv.writer(response)
            
            
            write_discrepancy_report(writer, snapshot_analysis, analysis1, plate)
                        
            if discrepancy != 'true':          
            
                write_full_analysis(writer, snapshot_analysis)
                
         
    except Exception: 
           
        print('exception: ', sys.exc_info)
        traceback.print_exc()

        return HttpResponse('bafle')


    return response



def write_discrepancy_report(writer, snapshot_analysis, analysis1, plate):

    writer.writerow(['', 'Discrepancy Report'])
    writer.writerow([])
    writer.writerow(['Copy ' + plate.stack.__str__() + " " + plate.__str__() ])
    writer.writerow([])
    writer.writerow([])


    
    for i in range(len(analysis1)):
    
        for j in range(len(analysis1[i])):
        
            snapshot_analysis[i][j][1] = analysis1[i][j]


            if snapshot_analysis[i][j][0] != analysis1[i][j]:

                if snapshot_analysis[i][j][0] == 0 and analysis1[i][j] == '':

                    continue

                print('snapshot_analysis[i][j][0]: ', snapshot_analysis[i][j][0] , '    analysis1[i][j]:', analysis1[i][j], '   ', type(analysis1[i][j]))


                m = 'The colony below is occupying a location which should be vacant'

                row = numberToLetterASCII(i)
                column = j+1

                locus = PlateLocus_Model.objects.filter(scheme = plate.scheme, row = row, column = column)

                strain = 'empty'

                if len(locus) > 0:

                    strain = locus[0].strain.name
                    m = 'The original library colony in the location below is gone'


                discrepancy_report = " row: " + row + " column: " + str(column) + "  strain: " + strain
                
                writer.writerow([m])
                writer.writerow([discrepancy_report])
                writer.writerow([])
                writer.writerow([])
                writer.writerow([])



def write_full_analysis(writer, snapshot_analysis):
    
    pr('yoobam')
    
    writer.writerow([])
    writer.writerow([])
    writer.writerow([])
    writer.writerow([])
    
    
    for j_row in snapshot_analysis:
    
        writer.writerow(j_row)




def libPattern(plate_scheme):

#     print('libPattern in views')
    
    lib_pattern = []
    
    format = plate_scheme.format
    
    width = format.width_loci
    length = format.length_loci
    
#     print('width: ', width, 'length: ', length)
    
        
    for i in range(length):
        
        b = []
        
        for j in range(width):
            
            b.append([0, 0])
            
        
        lib_pattern.append(b)     


    loci = PlateLocus_Model.objects.filter(scheme = plate_scheme) 

        
    for locus in loci:
        
        row = ord(locus.row.lower()) - 97
        column = locus.column - 1
        
#         print('row: ', row, 'column: ', column)
        
        lib_pattern[row][column][0] = 1

    
    return lib_pattern



def snapshot(request):
    """
    """
#     t0 = datetime.now()
#     print('str(t0):', str(t0))

    g = request.GET

    library = g.__getitem__('library')
#     print('library is: ', library)
    stack_name = g.__getitem__('stack')
#     print('stack_name is: ', stack_name)
    stack_pk = g.__getitem__('stack_pk')
#     print('stack_pk is: ', stack_pk)
    batch_num = g.__getitem__('batch_num')
    
    
    print('batch_num is: ', str(batch_num))
    plate_num = g.__getitem__('plate_num')
    print('plate_num is: ', str(plate_num))
    
    try:
        s = YeastPlateStack_Model.objects.get(pk=stack_pk)
        
        time_stamp = str(s.time_stamp)
#         
#         print(str(time_stamp))
        
    except Exception:
        
        print(sys.exc_info)
        traceback.print_exc()
     
    
    img_dict = {}
    img_dict['lib'] = library
    img_dict['stack'] = time_stamp
    img_dict['batch'] = batch_num
    img_dict['plate'] = plate_num
       
       
    cam = PlateCam()
       
    img_stored = False        
    img_version = 1
       
    sys_path, inner_path = views_util.validateStackDirs(library, time_stamp)
       
       
    pic_name = ''.join(['plate_', str(plate_num),'_batch_', str(batch_num), '_v_', str(img_version), '.jpeg'])
       
    print('pic_name: ', pic_name)
#     print('sys_path: ', sys_path)
           
    img_full_path = sys_path + '/' + pic_name
#     print('img_full_path: ', img_full_path)
           
    try:
        if cam.snapshot(img_full_path):
            img_stored = True
#             print('snapshot saved')
               
            browser_path = inner_path  + '/' +  pic_name
            print('browser_path: ', browser_path)
        else:
            print('cam did not take the picture')
            
    except Exception:        
        print(sys.exc_info())
        traceback.print_exc()
#         print('just printed exception')
        
        return HttpResponse('cam_error')

    if img_stored:
        
        s = str(img_dict).replace(', ', ',').replace(': ', ':')
#         print('img_dict to exiv: ', s)
        
        views_util.writeExiv(img_dict, img_full_path)

        
        snapshot, process_pk = views_util.analyseInBackground(stack_pk, plate_num, batch_num, browser_path, img_full_path)
        
    else:

        browser_path = '/static/image_analysis/failed_analysis.png'
           
    try:
        img_dict = {}
        img_dict['library'] = library
        img_dict['time_stamp'] = time_stamp
        img_dict['batch_num'] = batch_num
        img_dict['plate_num'] = plate_num
        img_dict['image_path'] = browser_path
        img_dict['snapshot_pk'] = snapshot.pk
        img_dict['stack'] = stack_name
        
        img_dict['process_pk'] = process_pk
        
        r = json.dumps(img_dict)
#         print('img_dict as json: ', r)
        
        
    except Exception:        
        print(sys.exc_info())
        traceback.print_exc()
#         print('just printed exception')
        
    response = HttpResponse(r)
       
    return response


def snapshot_follow_up(request):
    """
    """
    
    g = request.GET
    
    snapshot_pk = g.__getitem__('snapshot_pk')
#     print('snapshot_pk:', snapshot_pk)
    
    process_pk = g.__getitem__('process_pk')
#     print('process_pk:', process_pk)
    
    snapshot_process = SnapshotProcess_Model.objects.get(pk=snapshot_pk)
    
    status = snapshot_process.status
#     print('in snapshot_follow_up   snapshot_process.status:', status)
        
    response_dict = {}
    response_dict['status'] = status
    response_dict['process_pk'] = process_pk
    response_dict['snapshot_pk'] = snapshot_pk
    
    if status != 'bussy':
        
        snapshot = PlateSnapshot_Model.objects.get(pk=snapshot_pk)
        
        response_dict['processed_image_path'] = snapshot.processed_image_path
        response_dict['plate_index'] = snapshot.batch.plate.scheme.index
    
    #     pool = multiprocessing.Pool()
#     
#     try:
#         for process in pool.map:
#         
#             print('process.id: ', process.pid)
#     except Exception:        
#         print(sys.exc_info())
#         traceback.print_exc()
    
#     for cookie in request.COOKIES:
#         print('Cookie: ', cookie) 

    
    return HttpResponse(json.dumps(response_dict))



def lib_stack_map(request):
    """
    """
    try:
     
        if request.is_ajax():
            if request.method == 'POST':
            
                j = json.loads(request.body.decode("utf-8"))
            
                print('lib_stack_map got request: ', j)
                
                nicknames = j['nicknames']
                
                
    except Exception:
        print('exception: ', sys.exc_info)
        traceback.print_exc()
    
    
    d_lib_stack_map = {}
#     gridStackMap = util.getLibStackMap()

#   TODO make a more efficient query with Q

    if views_util.ALL_NICKNAMES in nicknames:
            
            libraries = YeastLibrary_Model.objects.order_by('name')            
            lib_stack_map_help(libraries, d_lib_stack_map)
            
    else:
    
        for nickname in nicknames:
            
#             print("nickname: ", nickname)
        
            libraries = YeastLibrary_Model.objects.filter(personal_name=nickname).order_by('name')
              
            lib_stack_map_help(libraries, d_lib_stack_map)
            
#         print('d_lib_stack_map:', d_lib_stack_map)
    
    
    storages = StorageLocation_Model.objects.all()    
    d_storages = []
    
    for storage in storages:
#         print('storage: ', storage.__str__())
        d_storages.append(storage.__str__())
    
#         print('storages list: ', d_storages)
         
    
    mediums = Batch_Model.objects.all()
    d_mediums = {}
    
    for medium in mediums:
        d_mediums[medium.__str__()] = medium.asDict()
    
    
    d_response = {}
    d_response['lib_stack_map'] = d_lib_stack_map
    d_response['storages'] = d_storages
    d_response['mediums'] = d_mediums
    
#         print('d_response', d_response)
    
    try:
        
        gridStackMap = json.dumps(d_response)
#             print('json version:', j)
    except Exception:
        print(sys.exc_info())
        traceback.print_exc()
        

#     print('gridStackMap: ')
#     print(gridStackMap)
    
    return HttpResponse(gridStackMap)



def lib_stack_map_help(libraries, d_lib_stack_map):

    for l in libraries:
                
        d_lib = l.asDict()
        
        d_stacks = {}
        
        stacks = YeastPlateStack_Model.objects.filter(library = l).order_by('time_stamp')
        
        for s in stacks:
            
#             print('s.time_stamp.timestamp():  ', s.time_stamp.timestamp())
#             print('s.asDict(): ', s.asDict())
            
            d_stacks[s.__str__()] = s.asDict()
        
        print('')
        
        d_lib['stacks'] = d_stacks
        
        d_lib_stack_map[l.name] = d_lib



def snapshot_model_map(request):
    """
    """    
#     print('snapshot_model_map()')
    
    g = request.GET
    
    personal_name = views_util.COMMON_USER
    
    try:
        personal_name = g.__getitem__('personal_name')
#         print('personal_name: ', personal_name)
        
        is_liquid = g.__getitem__('is_liquid')
#         print('is_liquid: ', is_liquid)
        
        
        if is_liquid == 'true':
            is_liquid = True
        else:
            is_liquid = False
        
        
    except Exception:
        print('exception: ', sys.exc_info)
        traceback.print_exc()
        
        
    libraries = YeastLibrary_Model.objects.filter(personal_name=personal_name)
    d_snapshot_model_map = {}
      
    l_helper = LibraryHelper() 
      
    for l in libraries:
        
        d_snapshot_model_map[l.__str__()] = l_helper.getPlateMap(l, is_liquid)
    
            
#         print('d_snapshot_model_map:', d_snapshot_model_map)
    
    try:
        
        snapshot_model_map = json.dumps(d_snapshot_model_map)
#             print('json version:', j)
    except Exception:
        print(sys.exc_info())
        
        
#     snapshot_model_map = util.getSnaphotModelMap(personal_name, is_liquid)
    
    return HttpResponse(snapshot_model_map)


def snapshot_map(request):
    """
    """    
#     print('snapshot_model_map()')
    
    g = request.GET
    
    try:
        plate_pk = g.__getitem__('plate_pk')
        print('plate_pk: ', plate_pk)
        
    
    
        plate = YeastPlate_Model.objects.get(pk=plate_pk)

    
    except Exception:
        print('exception: ', sys.exc_info)
        traceback.print_exc()
    

    snapshot_model_map = get_plate_snapshots(plate)
    
    return HttpResponse(json.dumps(snapshot_model_map))


def plate_map(request):
    """
    """   
    
    pr("entered")
    
    try:
     
        if request.is_ajax():
            if request.method == 'POST':
            
                j = json.loads(request.body.decode("utf-8"))
            
                pr('request json: ' + str(j))
                
                nicknames = j['nicknames']
        #         print('personal_name: ', personal_name)
                
                is_liquid = j['is_liquid']
#                 print('  jamzee is_liquid: ', is_liquid)
                
                
    except Exception:
        print('exception: ', sys.exc_info)
        traceback.print_exc()
        
    
    try:
        l_helper = LibraryHelper()
        d_plate_maps = l_helper.getPlateMaps(nicknames, is_liquid)
        
        plate_map = json.dumps(d_plate_maps)
#             print('json version:', j)
    except Exception:
        print(sys.exc_info())
        
#     print('plate_map: ', plate_map) 
#     snapshot_model_map = util.getSnaphotModelMap(personal_name, is_liquid)
    
    return HttpResponse(plate_map)




def get_plate_snapshots(plate):
    
    try:
    
        d_plate = plate.getDataShellDict()
    
    except Exception:
        print('exception: ', sys.exc_info)
        traceback.print_exc()
    
    
    batches = SnapshotBatch_Model.objects.filter(plate=plate).order_by('index')
    
    
    batches_map = []
    
    b_helper = SnapshotBatchHelper()
    
    
    for batch in batches:
        
        batches_map.append(b_helper.getBareDict(batch))
         
#         print('d_snapshot_model_map:', d_snapshot_model_map)
    
    d_plate['batches'] = batches_map


    return d_plate
    



def copy_snapshot_map(request):
    """
    """   
    
    g = request.GET
    
    try:
        copy_pk = g.__getitem__('copy_pk')
#         print('copy_pk: ', copy_pk)
        
        copy = YeastPlateStack_Model.objects.get(pk=copy_pk)
        plates = YeastPlate_Model.objects.filter(stack=copy).order_by('scheme__index')
        
    except Exception:
        print('exception: ', sys.exc_info)
        traceback.print_exc()       
        
        
    snapshot_model_map = []
    
    for plate in plates:
    
        plate_map = get_plate_snapshots(plate)
        snapshot_model_map.append(plate_map)
        
    
    #     print('snapshot_model_map()')
    
    return HttpResponse(json.dumps(snapshot_model_map))





def private_lib_list(request):
    """
    """
#     print('private_lib_list')
    
    re = []
    
    try:
        private_libs = YeastLibrary_Model.objects.exclude(personal_name = views_util.COMMON_USER)
    
        for l in private_libs:
            
            if not l.personal_name in re:
                   
                re.append(l.personal_name)
            
    except Exception:
        print('exception: ', sys.exc_info)
        traceback.print_exc()
    
    

       
    return HttpResponse(json.dumps(re)) 

    
    
def stack_register(request):
    """
    """
    
    if request.method == 'POST':
    
        print('')
        
#         for key in request.FILES.keys():
#             print('key: ' + key)
#             print('file_name: ' + str(request.FILES[key]))
 
        p = request.POST

        
        try:
            
            s_library = int(p.__getitem__('library'))
#         print('library: ', s_library)
            
            is_liquid = p.__getitem__('is_liquid')
#             print('is_liquid: ', is_liquid)
            
            if is_liquid == 'true':
                is_liquid = True
            else:
                is_liquid = False

            s_time = p.__getitem__('time')
            print('time: ', s_time)
            
            s_medium = p.__getitem__('medium')
    #         print('medium: ', s_medium)
            
            s_comments = p.__getitem__('comments')
    #         print('comments: ', s_comments)
            
            s_storage = p.__getitem__('storage')
    #         print('storage: ', s_storage)
        except Exception:
            print('exception: ', sys.exc_info)
            traceback.print_exc()
            
        try:
            
            s_stack_pk = int(p.__getitem__('stack'))
#             print('s_stack_pk: ', s_stack_pk)

        except Exception:
            print('exception: ', sys.exc_info)
            traceback.print_exc()
            s_stack_pk = 0
            
            
    r = register_stack(s_library, is_liquid, s_time, s_medium, s_comments, s_storage, s_stack_pk)       
    
    return HttpResponse(json.dumps(r))
    
            
            
def register_stack(s_library, is_liquid, s_time, s_medium, s_comments, s_storage, s_stack_pk):        
        
    s = s_time.split()
    
    s_date = s[0].replace('/', '-')
    s_watch = s[1]
    
    ss = s_date.split('-')
    s_year = ss[0]
    s_month = ss[1]
    s_day = ss[2]
    
    ss = s_watch.split(':')
    s_hour = ss[0]
    s_minute = ss[1]
    
    try:
        
        print('year = ', s_year, 'day = ', s_day, 'month = ', s_month, 'hour = ', s_hour, 'minute = ', s_minute)
        
        time_stamp = datetime(year = int(s_year), day = int(s_day), month = int(s_month), hour = int(s_hour), minute = int(s_minute))
        print('time_stamp: ', time_stamp.__str__())

    
    
        library = YeastLibrary_Model.objects.get(pk = s_library)


        parent_stack = None

        if s_stack_pk != 0:

            parent_stack = YeastPlateStack_Model.objects.get(pk = s_stack_pk)
    #             print('parent_stack.__str__(): ', parent_stack.__str__())


        medium = Batch_Model.objects.get(pk=int(s_medium))
        storage = StorageLocation_Model.objects.get(location = s_storage)

    except Exception:
        print(sys.exc_info())
        traceback.print_exc()

    
    try:
        stack, created = YeastPlateStack_Model.objects.get_or_create(time_stamp = time_stamp, library = library, storage = storage, medium = medium, parent = parent_stack, is_liquid=is_liquid)
    except Exception:
        print('exception: ', sys.exc_info)
        traceback.print_exc()
        
        er = {}
        er['error'] = 'same_time_error'
        return HttpResponse(json.dumps(er)) 
    
    
    
    if created:
        pass
#             print('stack was created') 
    else:
#             print('stack wasnt created')
        
        er = {}
        er['error'] = 'same_time_error'
        return HttpResponse(json.dumps(er)) 


    plate_schemes = PlateScheme_Model.objects.filter(library = library)
#         print('type of plate schemes:  ', type(plate_schemes))

    
    try:
#         create stack plates
        for plate_scheme in plate_schemes:
#                 print('plate scheme:', plate_scheme.__str__())
             
            plate, created = YeastPlate_Model.objects.get_or_create(
                stack = stack,                                                    
                scheme = plate_scheme,
                time_stamp = time_stamp,
                user = 'mishehoo',
                conditions = s_comments,
            )
            
            
            if is_liquid:
                
                liquid_plate, created = LiquidYeastPlate_Model.objects.get_or_create(yeast_plate=plate)
            
            if created:
                 
                print('')
                print(plate.__str__(), '  was just created')
                print('')
            else:
                print('plate wasnt created')
                
    except Exception:
        
        print('exception: ', sys.exc_info)
        traceback.print_exc()

    r = {}
    r['library_name'] = library.name
    r['library_pk'] = library.pk
    
    
    s_helper = CopyHelper()
    
    r['new_stack'] = s_helper.getBareDict(stack)
    
    return r




def stack_register_gui(request):
    """
    """
    
    return render_to_response(
            'yeast_libraries/stack_register.html',
            {},
            context_instance=RequestContext(request)
        )




@never_cache
def library_copier(request):

    # print('request')
    # print(request)


    if request.method == 'POST':
        
#         print('library_copier fantastic')
#         print('')
        
#         for t in request.POST.items():  #this was the probelmatic code
#             print('tuple: ', str(t))
        
        try:
            p = request.POST
            personal_name = p.__getitem__('personal_name')
#             print('personal_name: ', personal_name)            
            
        except Exception:
            print('exception: ', sys.exc_info)
            traceback.print_exc()
        
        
        
        
#         print('request.FILES: ', request.FILES)
#         print('')
        
#         for key in request.FILES.keys():
#             print('key: ' + key)
            
        data = request.FILES['input_file']
        
#         print(data.name)
#         print('data type:', type(data))
        
#         print('data.read() type: ', type(data.read()))
        
        if data.name[-3:]=='xls':
            
            libraryParcer = LibraryParser()
            try:
                libraryParcer.libraryExcelParser(data, personal_name)
            except Exception:
                print('exception: ', sys.exc_info)
                traceback.print_exc()
                
        
        return HttpResponse('successfully processed excel: ' + data.name)
        
    else:
        response =  render_to_response(
            'yeast_libraries/library_copier.html',
            {},
            context_instance=RequestContext(request)
        )

        # response['Cache-Control'] = 'no-cache'
        # print('response')
        # print(response.content.decode(encoding='UTF-8'))

        return response
             
    
def show_analysis(request):
    """
    """
    
#     print('show_analysis')
    
    return render_to_response(
            'yeast_libraries/show_analysis.html',
            {},
            context_instance=RequestContext(request)
        ) 
    


def cam(request):
    """
    """
    
    return render_to_response(
            'yeast_libraries/cam.html',
            {},
            context_instance=RequestContext(request)
        ) 
    
    
    
def simple_snapshot(request):
    """
    """
#     print('')
#     print('reached simple snapshot')
#     print('')

    g = request.GET
    
    pic_name = 'stam.jpg' #g.__getitem__('pic_name')
#     print('pic_name is: ', pic_name)
    
    
    cam = PlateCam()
       
       
    try:
        inner_path = 'noa_dafis'
        sys_path = os.path.join('/cs/wetlab/yeast_library_images', inner_path)  
           
        if not os.path.exists(sys_path):
            os.makedirs(sys_path)
                           
    except Exception:        
        print(sys.exc_info())
        print('just printed exception')
       
    
#     print('pic_name: ', pic_name)
#     print('inner_path: ', inner_path)
#     print('sys_path: ', sys_path)
           
    img_full_path = sys_path + '/' + pic_name
#     print('img_full_path: ', img_full_path)
       
           
    try:
        if cam.snapshot(img_full_path):
            img_stored = True
#             print('snapshot saved')
               
            browser_path = '/media/' + inner_path  + '/' +  pic_name
#             print('browser_path: ', browser_path)
    except Exception:        
        print(sys.exc_info())
        print('just printed exception')
        return HttpResponse('cam_error')
                   
           
    if img_stored:
          
        d_response = {}
        d_response['image_path'] = browser_path
        
        r = json.dumps(d_response)
#         print('img_dict as json: ', r)

        
    response = HttpResponse(r)
       
    return response



def get_image(request):
    """
    """
#     print('')
#     print('reached getImage')
#     print('')
    
    g = request.GET
    
    relative_path = g.__getitem__('image_full_path')
#     print('relative_path:', relative_path)
    full_path = os.path.join(settings.PLATE_IMAGE_ROOT, relative_path)
#     print('full_path: ', full_path)
    
    try:
        image_data = open(full_path, "rb").read()
        
    except Exception:
        print('exception: ', sys.exc_info)
        traceback.print_exc() 
        
        print('because of error returning default image')
        
        try:
            path = os.path.join(settings.STATIC_ROOT, 'yeast_libraries/img/empty.png')
            
#             print('returning empty')
            
            image_data = open(path, "rb").read()
            return HttpResponse(image_data, content_type="image/png")
        
        except Exception:
            print('exception: ', sys.exc_info)
            traceback.print_exc() 
    
    return HttpResponse(image_data, content_type="image/jpeg")


def annoymous_snapshot(request):
    """
    """
#     print('')
#     print('reached annoymous_snapshot')
#     print('')
    

    full_path = os.path.join(settings.PLATE_IMAGE_ROOT, 'noa_dafis')
       
    try:
           
        if not os.path.exists(full_path):
            os.makedirs(full_path)
                           
    except Exception:        
        print(sys.exc_info())
        print('')
        
    img_full_path = os.path.join(full_path, 'stam.jpg')
    print('img_full_path: ', img_full_path)
           
    try:
        cam = PlateCam()
        
        if cam.snapshot(img_full_path):
            img_stored = True
#             print('snapshot saved')
            
    except Exception:        
        print(sys.exc_info())
        print('just printed exception')
        return HttpResponse('cam_error')
    
    try:
        image_data = open(img_full_path, "rb").read()
        
    except Exception:
        print('exception: ', sys.exc_info)
        traceback.print_exc() 
        
        print('because of error returning default image')
        
        try:
            path = os.path.join(settings.STATIC_ROOT, 'yeast_libraries/img/empty.png')
            
            image_data = open(path, "rb").read()
            return HttpResponse(image_data, content_type="image/png")
        except Exception:
            print('exception: ', sys.exc_info)
            traceback.print_exc() 
    
    return HttpResponse(image_data, content_type="image/jpeg")



    
def get_plate_pattern(request):  

    try:
        g = request.GET      
        plate_pk = g.__getitem__('plate_pk')
        
        plate = YeastPlate_Model.objects.get(pk=plate_pk)
    
        scheme = plate.scheme
        
        format = scheme.format
        
        
        width = format.width_loci
        length = format.length_loci
        
#         print('width: ', width, 'length: ', length)
        
        loci_ = []
        
        for i in range(length):
            loci_.append([0]*width) 
    
        
        
        loci = PlateLocus_Model.objects.filter(scheme = scheme)
    
        pattern = {}
        
        pattern['width'] = width
        pattern['height'] = length 
     
     
        for locus in loci:
             
            locus_ = {}
            locus_['strain'] = locus.strain.name
            locus_['column'] = locus.column
            locus_['row'] = locus.row
            locus_['pk'] = locus.pk
            
#             print('row', locus.row, ' column', locus.column)
            
            loci_[locus.rowAsNum() - 1][locus.column - 1] = locus_
             
        pattern['loci'] = loci_
        
    except Exception:
        print('exception: ', sys.exc_info)
        traceback.print_exc() 
    
    
    return HttpResponse(json.dumps(pattern))
    
    