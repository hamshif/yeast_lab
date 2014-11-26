import sys, os, traceback, subprocess, psycopg2, multiprocessing, shutil

from datetime import datetime

from lab import settings
from yeast_libraries.models import YeastLibrary_Model, YeastPlateStack_Model,\
    SnapshotBatch_Model, YeastPlate_Model, PlateSnapshot_Model,SnapshotProcess_Model,\
    LocusAnalysis_Model, StorageLocation_Model
from cmd_utils.exiv2 import Exiv2

from image_analysis.image_processor import ImageAnalysisControler
from lab_util.util import pr

from yeast_libraries.views import register_stack

from django.utils.timezone import utc
from yeast_libraries import views_util


def ge():
    ''
    path = '/cs/wetlab/dev_yeast_library_images/'
#     semantic_path = 'KOShai_yldb_ver/copy/2014-08-18 12:00:00'
#     semantic_path = 'KOShai_yldb_ver/copy/2014-02-16 12:00:00'
    semantic_path = 'KOShai_yldb_ver/copy/2014-04-07 12:00:00'
    
    
    imageAnalysisFromFolder(path, semantic_path)


def imageAnalysisFromFolder(path, semantic_path):
        
#     print('')
#     print('reached snapshot')
#     print('')
    semantics = semantic_path.split('/')

    library_name = semantics[0]
    print('library is: ', library_name)
    stack_time = semantics[2]
    print('stack_time is: ', stack_time)
    
    library = YeastLibrary_Model.objects.get(name = library_name)
    print("library.pk: ", library.pk)
    
    s = stack_time.split()
        
    s_date = s[0].replace('/', '-')
    s_watch = s[1]
    
    ss = s_date.split('-')
    s_year = ss[0]
    
    print("s_year: ", s_year)
    
    s_month = ss[1]
    s_day = ss[2]
    
    ss = s_watch.split(':')
    s_hour = ss[0]
    s_minute = ss[1]
    
    try:
#             print('year = ', s_year, 'day = ', s_day, 'month = ', s_month, 'hour = ', s_hour, 'minute = ', s_minute)
        
        time_stamp = datetime(year = int(s_year), day = int(s_day), month = int(s_month), hour = int(s_hour), minute = int(s_minute))
        print('time_stamp before: ', time_stamp)

        time_stamp = time_stamp.replace(tzinfo=utc)
        print('time_stamp timezoned: ', time_stamp)   

        
        stack = YeastPlateStack_Model.objects.get(time_stamp = time_stamp, library = library)
        time_stamp = s.time_stamp
        
        print("stack.pk: ", stack.pk)
        
    except Exception:
        print(sys.exc_info())
    
    try:
#        
#         print('settings.PLATE_IMAGE_ROOT: ', settings.PLATE_IMAGE_ROOT)
        sys_path = os.path.join(path, semantic_path)
#         sys_path = os.path.join('/cs/wetlab/yeast_library_images', inner_path)   
        print("sys_path: ", sys_path)
        
           
        if not os.path.exists(sys_path):
#             os.makedirs(sys_path)
            ''
            print('path: ', sys_path, '  does not exist')

        else:
            
            imageAnalysisControler = ImageAnalysisControler()
            
            print('path: ', sys_path, '  exists')
                
            for root, dirs, files in os.walk(sys_path):
                
#                     print("Current directory: " + root)
#                     print("Sub directories: " + str(dirs))
#                     print("Files: " + str(files))
                # this is to save versions of images
                for f in files: 
                    
                    if f[-5:] != "p.jpg" and f[0] != '.':
                    
                        print('file_name:', f)
                        semantic = str(f)[0:-5].split('_')
                        
                        print("   plate_num : ",  semantic[1])
                        print("   batch_num : ",  semantic[3])
                          
                        plate_num = int(semantic[1])
                        batch_num = int(semantic[3])
                         
                        
                     
                        plate = YeastPlate_Model.objects.get(stack = stack, scheme__index = plate_num)
           
#                         exiv2 = Exiv2()
                         
                        img_full_path = sys_path + '/' + f
                         
                         
#                         meta_data = exiv2.getComment(img_full_path)
#        
#                         print('imageAnalysisFromFolder:', datetime.now(), '    finished meta_data:', meta_data)
 
                           
                        snapshot_batch, created = SnapshotBatch_Model.objects.get_or_create(plate = plate, index = batch_num)
            
                        print('str(snapshot_batch.pk): ', str(snapshot_batch.pk))
                          
                        if created:
                            print('just created snapshot_batch #', batch_num, 'for', plate.__str__())
                        else:
                            print('just retrieved snapshot_batch #', batch_num, 'for', plate.__str__())
                        browser_path = semantic_path  + '/' +  f
            
                        snapshot, created = PlateSnapshot_Model.objects.get_or_create(batch = snapshot_batch, image_path = browser_path)
           
                        print('str(snapshot_batch.pk): ', str(snapshot_batch.pk))
                         
                         
                         
                        snapshot.time_stamp = datetime.now()
                        snapshot.save()
                         
                        snapshot_process, created = SnapshotProcess_Model.objects.get_or_create(snapshot_pk=snapshot.pk)
                          
            #             if created:
            #                 print('snapshot_process.__str__(): ', snapshot_process.__str__(), ' was just created')
            #                  
            #             else:
            #                 print('snapshot_process.__str__(): ', snapshot_process.__str__(), ' was just retrieved')
            #                  
            #                 if snapshot_process.status == 'bussy':
            #                     print('a former process is probably still working on analyzing the pic')
                         
             
                        snapshot_process.status = 'bussy'
                        snapshot_process.save()   
              
                        process_pk = snapshot_process.pk
                         
                        print('')
                        print('starting process')
                         
                        process_table_name = snapshot_process._meta.db_table
                        db_name = settings.DB_NAME
                        
                        
                        imageAnalysisControler.processImage(imageAnalysisControler, settings.BASE_DIR, settings.PLATE_IMAGE_ROOT, img_full_path, snapshot.pk, process_pk, db_name, process_table_name)
                        
                        
#                         process = multiprocessing.Process(target=ImageAnalysisControler.processImage, args=(imageAnalysisControler, settings.BASE_DIR, settings.PLATE_IMAGE_ROOT, img_full_path, snapshot.pk, process_pk, db_name, process_table_name))
#                         process.start()
             
    except Exception:        
        print(sys.exc_info())
        print('just printed exception')
        traceback.print_exc()

              
def reAnalyseSnapshot(plate_pk, batch_index):
    
    ''
    
    try:
        
        snapshot = PlateSnapshot_Model.objects.get(batch__plate__pk = plate_pk, batch__index = batch_index)
        plate = snapshot.batch.plate
        stack = plate.stack
        
        print(stack.__str__())
        print(plate.__str__())
        print("snapshot.pk: ", snapshot.pk)
        
#         analyses = LocusAnalysis_Model.objects.filter(snapshot = snapshot).delete()
        
        snapshot_process, created = SnapshotProcess_Model.objects.get_or_create(snapshot_pk=snapshot.pk)
                            
             
        snapshot_process.status = 'bussy'
        snapshot_process.save()   
     
        process_pk = snapshot_process.pk
        
        print('')
        print('starting process')
        
        process_table_name = snapshot_process._meta.db_table
        db_name = settings.DB_NAME
       
        imageAnalysisControler = ImageAnalysisControler()
        
        img_full_path = settings.PLATE_IMAGE_ROOT + '/' + snapshot.image_path
        
        pr(img_full_path)
         
        imageAnalysisControler.processImage(settings.BASE_DIR, settings.PLATE_IMAGE_ROOT, img_full_path, snapshot.pk, process_pk, db_name, process_table_name)

    except Exception:        
        print(sys.exc_info())
        print('just printed exception')
        traceback.print_exc()
    


def deleteSnapshots(batch):
    
    snapshots = batch.snapshots.all();
    
    
    for snapshot in snapshots:
        
        loci = snapshot.analysis.all()
        
        loci.delete()
        
        
        snapshot.delete()
        
    batch.snapshots.clear()
    
    batch.save()
        
    
def deleteStackIfNoSnapshots(stack):
    
    
    if stack.is_liquid == True:
        
        print(stack.__str__() + ' is liquid and wont be deleted')
        return
        
    
    snapshots = PlateSnapshot_Model.objects.filter(batch__plate__stack=stack)
    
    if len(snapshots)==0:
        
        print(stack.__str__() + ' does not have snapshots')
        stack.delete()
        
        
    else:
        print(stack.__str__() + ' has ' + str(len(snapshots)) + ' snapshots and wont be deleted')
    
    
def allStacks():
    
    stacks = YeastPlateStack_Model.objects.all()
    
    for stack in stacks:
        
        deleteStackIfNoSnapshots(stack)
    
    

    
    
    
    
    
    
        
def clearDB():
    
    try:
        con = psycopg2.connect(host = 'cab-27', database=settings.DB_NAME, user='gideonbar') 
        cur = con.cursor()
        
        tables = (
#             'auth_group', 'auth_group_id_seq', 'auth_group_permissions', 'auth_group_permissions_id_seq', 'auth_permission', 'auth_permission_id_seq', 
#             'auth_user', 'auth_user_groups', 'auth_user_groups_id_seq', 'auth_user_id_seq', 
#             'auth_user_user_permissions', 'auth_user_user_permissions_id_seq', 'django_admin_log', 'django_admin_log_id_seq', 
#             'django_content_type', 'django_content_type_id_seq', 'django_session', 
            'mediums_batch_model', 
            'mediums_batch_model_compounds', #'mediums_batch_model_compounds_id_seq', 'mediums_batch_model_id_seq', 
            'mediums_chemicalcompound_model', #'mediums_chemicalcompound_model_id_seq', 
            'mediums_compound_model', #'mediums_compound_model_id_seq', 
            'suppliers_source_model', #'suppliers_source_model_id_seq', 
            'yeast_libraries_locusanalysis_model', #'yeast_libraries_locusanalysis_model_id_seq',
            'yeast_libraries_plateformat_model', #'yeast_libraries_plateformat_model_id_seq', 
            'yeast_libraries_platelocus_model', #'yeast_libraries_platelocus_model_id_seq', 
            'yeast_libraries_platescheme_model',
            #'yeast_libraries_platescheme_model_id_seq', 
            'yeast_libraries_platescheme_model_loci', 
            #'yeast_libraries_platescheme_model_loci_id_seq', 
            'yeast_libraries_platesnapshot_model', 
            'yeast_libraries_platesnapshot_model_analysis', #'yeast_libraries_platesnapshot_model_analysis_id_seq', 
            #'yeast_libraries_platesnapshot_model_id_seq', 
            'yeast_libraries_snapshotbatch_model',
            #'yeast_libraries_snapshotbatch_model_id_seq', 
            'yeast_libraries_snapshotbatch_model_snapshots', 
            #'yeast_libraries_snapshotbatch_model_snapshots_id_seq', 
            'yeast_libraries_snapshotprocess_model',
            #'yeast_libraries_snapshotprocess_model_id_seq', 
            'yeast_libraries_storagelocation_model' , 
            #'yeast_libraries_storagelocation_model_id_seq',
            'yeast_libraries_yeastlibrary_model', 
            #'yeast_libraries_yeastlibrary_model_id_seq', 
            'yeast_libraries_yeastlibrary_model_plate_schemes',
            #'yeast_libraries_yeastlibrary_model_plate_schemes_id_seq', 
            'yeast_libraries_yeastlibrary_model_stacks', 
            #'yeast_libraries_yeastlibrary_model_stacks_id_seq',
            'yeast_libraries_yeastplate_model', 
            #'yeast_libraries_yeastplate_model_id_seq', 
            'yeast_libraries_yeastplate_model_snapshot_batches',
            #'yeast_libraries_yeastplate_model_snapshot_batches_id_seq', 
            'yeast_libraries_yeastplatestack_model', 
            #'yeast_libraries_yeastplatestack_model_id_seq',
            'yeast_libraries_yeastplatestack_model_plates', 
            #'yeast_libraries_yeastplatestack_model_plates_id_seq', 
            'yeast_libraries_yeaststrain_model',
            #'yeast_libraries_yeaststrain_model_id_seq', 
            'yeast_libraries_yeaststrain_model_parents', 
            #'yeast_libraries_yeaststrain_model_parents_id_seq'
            
            'yeast_liquid_plates_spctrometersample_model',
            'yeast_liquid_plates_spectrometerexperiment_model',
            'yeast_liquid_plates_spectrometerprocedure_model',
            'yeast_liquid_plates_spectrometerwelldata_model',
            
            
             'yeast_liquid_plates_liquidprocedure_model',
             
             'yeast_liquid_plates_liquidyeastplate_model',
            
            'yeast_liquid_plates_parsedataprocess_model', 
            
            
            'lab_experimentschedule_model',
            'lab_hardwareconfig_model',
        )
        
        for table in tables:
            
            cur.execute('DROP TABLE IF EXISTS ' + table + ' CASCADE')
            
        con.commit()
        
        
        sequences = (
#             'auth_group', 'auth_group_id_seq', 'auth_group_permissions', 'auth_group_permissions_id_seq', 'auth_permission', 'auth_permission_id_seq', 
#             'auth_user', 'auth_user_groups', 'auth_user_groups_id_seq', 'auth_user_id_seq', 
#             'auth_user_user_permissions', 'auth_user_user_permissions_id_seq', 'django_admin_log', 'django_admin_log_id_seq', 
#             'django_content_type', 'django_content_type_id_seq', 'django_session', 

            'lab_experimentschedule_model_id_seq',
            'lab_hardwareconfig_model_id_seq',

            'mediums_batch_model_compounds_id_seq', 'mediums_batch_model_id_seq', 
            'mediums_chemicalcompound_model_id_seq', 
            'mediums_compound_model_id_seq', 
            'suppliers_source_model_id_seq', 
            'yeast_libraries_locusanalysis_model_id_seq',
            'yeast_libraries_plateformat_model_id_seq', 
            'yeast_libraries_platelocus_model_id_seq', 
            'yeast_libraries_platescheme_model_id_seq',
            'yeast_libraries_platescheme_model_loci_id_seq', 
            'yeast_libraries_platesnapshot_model_analysis_id_seq', 
            'yeast_libraries_platesnapshot_model_id_seq', 
            'yeast_libraries_snapshotbatch_model_id_seq', 
            'yeast_libraries_snapshotbatch_model_snapshots_id_seq', 
            'yeast_libraries_snapshotprocess_model',
            'yeast_libraries_snapshotprocess_model_id_seq', 
            'yeast_libraries_storagelocation_model_id_seq',
            'yeast_libraries_yeastlibrary_model_id_seq',
            'yeast_libraries_yeastlibrary_model_plate_schemes_id_seq', 
            'yeast_libraries_yeastlibrary_model_stacks_id_seq',
            'yeast_libraries_yeastplate_model_id_seq', 
            'yeast_libraries_yeastplate_model_snapshot_batches_id_seq', 
            'yeast_libraries_yeastplatestack_model_id_seq',
            'yeast_libraries_yeastplatestack_model_plates_id_seq', 
            'yeast_libraries_yeaststrain_model_id_seq', 
            'yeast_libraries_yeaststrain_model_parents_id_seq',
            
            'yeast_liquid_plates_spctrometersample_model_id_seq',
            'yeast_liquid_plates_spectrometerexperiment_model_id_seq',
            'yeast_liquid_plates_spectrometerprocedure_model_id_seq',
            'yeast_liquid_plates_spectrometerwelldata_model_id_seq',
            'yeast_liquid_plates_liquidprocedure_model_id_seq',
            
            'yeast_liquid_plates_parsedataprocess_model_id_seq',
        )
        
        for seq in sequences:
            
            cur.execute('DROP SEQUENCE IF EXISTS ' + seq + ' CASCADE')
            
        con.commit()


        subprocess.call(["rm", "-rf", "/cs/system/gideonbar/dev/workspace/lab/src/yeast_libraries/migrations/"])

        subprocess.call(["python3.3", "manage.py", "migrate"])

        cur.execute('GRANT ALL ON yeast_libraries_platelocus_model TO wetlab')
        cur.execute('GRANT ALL ON yeast_libraries_platelocus_model_id_seq TO wetlab')
        cur.execute('GRANT ALL ON yeast_libraries_snapshotprocess_model TO wetlab')
        cur.execute('GRANT ALL ON yeast_libraries_locusanalysis_model TO wetlab')
        cur.execute('GRANT ALL ON yeast_libraries_locusanalysis_model_id_seq TO wetlab')
        cur.execute('GRANT ALL ON yeast_libraries_platesnapshot_model TO wetlab')
        cur.execute('GRANT ALL ON yeast_libraries_platesnapshot_model_id_seq TO wetlab')
        cur.execute('GRANT ALL ON yeast_libraries_snapshotbatch_model TO wetlab')
        cur.execute('GRANT ALL ON yeast_libraries_snapshotbatch_model_id_seq TO wetlab')
        cur.execute('GRANT ALL ON yeast_libraries_yeastplate_model TO wetlab')
        cur.execute('GRANT ALL ON yeast_libraries_yeastplate_model_id_seq TO wetlab')
        cur.execute('GRANT ALL ON yeast_libraries_platescheme_model TO wetlab')
        cur.execute('GRANT ALL ON yeast_libraries_platescheme_model_id_seq TO wetlab')

        con.commit()


        cur.execute("CREATE OR REPLACE VIEW snapshot_scheme AS SELECT yeast_libraries_platesnapshot_model.id AS snapshot_id, yeast_libraries_snapshotbatch_model.id AS batch_id, yeast_libraries_yeastplate_model.id AS plate_id, yeast_libraries_platescheme_model.id AS scheme_id FROM yeast_libraries_platesnapshot_model JOIN yeast_libraries_snapshotbatch_model ON yeast_libraries_platesnapshot_model.batch_id = yeast_libraries_snapshotbatch_model.id JOIN yeast_libraries_yeastplate_model ON yeast_libraries_snapshotbatch_model.plate_id = yeast_libraries_yeastplate_model.id JOIN yeast_libraries_platescheme_model ON yeast_libraries_yeastplate_model.scheme_id = yeast_libraries_platescheme_model.id;")

        con.commit()

        cur.execute('GRANT ALL ON snapshot_scheme TO wetlab')

        print('granted permissions')


        import db_config


    except Exception:
        print('exception: ', sys.exc_info)
        traceback.print_exc()
        
    finally:
        if con:
            con.close()




# This is for parsing reading copying renaming analyzing and storing old images
# caution is advised due to variance in user image naming
def A(path="/cs/wetlab/Ayelet/Libraries/KO_Shai/KO_Shai_Images/KO_Shai22.1.12", library_name="KO_Shai", given_name="KO_Shai"):


    imageAnalysisFromFolder1(path=path, library_name=library_name, given_name=given_name, foreground=False, os_type='linux')



# This is for parsing reading copying renaming analyzing and storing old images
# caution is advised due to variance in user image naming
# this is a batch operation using slurm extra caution
def batchA():
    
    given_name = "KO_Shai"
    path = "/cs/wetlab/Ayelet/Libraries/KO_Shai/KO_Shai_Images"
    
    for root, dirs, files in os.walk(path):
    #         print('')
    
        cdir = root.split('/')[-1]
    
    
        if not given_name in cdir:
            
            continue
        
        elif path == root:
            
            continue
        
        print("Current directory: " + root)


        try:

            con = psycopg2.connect(host = 'pghost', database='ribs')

        
            imageAnalysisFromFolder1(root, "KO_Shai", given_name, foreground = False, os_type = 'linux', out_con=con)


        #         print("Sub directories: " + str(dirs))
        #         print("Files: " + str(files))

    #         for f in files:
    #
    #             semantic = str(f)
    #             print("Current directory: " + root)
    #             print('file name: ', semantic)
        
        except Exception:
            print('exception: ', sys.exc_info)
            traceback.print_exc()


        finally:

            if con:

                con.close()


def imageAnalysisFromFolder1(path, library_name, given_name, foreground = True, os_type = 'FreeBSD', out_con = None):
    
    
    try:
    
        library = YeastLibrary_Model.objects.get(name = library_name)
        
        print('library.__str__(): ', library.__str__())
        
        
        print('path')
        print(path)
        
        
        raw_date = path.split('/')[-1]
        
        raw_date = raw_date.replace(given_name, "")
        
        print('raw_date:', raw_date)
        
        raw_day, raw_month, raw_year = raw_date.split('.')
        
        
        
        time_stamp = datetime(year = int("20" + raw_year), day = int(raw_day), month = int(raw_month), hour = 12, minute = 0)
        print(time_stamp)
        
        
        s_storage = "Refrigerator"
        s_comments = "Added automatcally from directory"
        
        s_library = library.pk
        is_liquid = False
        
        s_time = "20" + raw_year + '/' + raw_month + '/' + raw_day + ' 12:00'                  
#           2014/02/14 15:00

        s_stack_pk = 0
        s_medium = "1"
        
        
       
        r = register_stack(s_library, is_liquid, s_time, s_medium, s_comments, s_storage, s_stack_pk)
        
#         pr(str(r))
           
        
        stack = YeastPlateStack_Model.objects.get(library=library, time_stamp=time_stamp)
        
        print(stack.__str__())
        
        sys_path, inner_path = views_util.validateStackDirs(library_name, str(time_stamp))

        
        for root, dirs, files in os.walk(path):
    #         print('')
    #         print("Current directory: " + root)
    #         print("Sub directories: " + str(dirs))
    #         print("Files: " + str(files))
            
            for f in files: 
                 
                semantic = str(f)
                
                if(semantic[0] == "."):
                    
                    pr(semantic + " is a hidden file")
                    continue
                
#                 print("Current directory: " + root)
#                 print('file name: ', semantic)
                
                semantic = semantic.split(sep="_")
#                 print('semantic: ', semantic)
                
                s_plate = semantic[-1].split(sep=".")[0]
                
                i = 0
                
                for ch in s_plate:
                    
                    if ch != '0':
                    
                        break
                    
                    i = i+1    
                
                s_plate = s_plate[i:]
#                 print('s_plate: ', s_plate)
                
                batch_num = 1
                
                if 'a' in s_plate:
                    
                    batch_num = 2
                    s_plate = s_plate.replace("a", "")
                    
                
                
                pic_name = ''.join(['plate_', s_plate,'_batch_', str(batch_num), '_v_', '1', '.jpeg'])
               
#                 print('pic_name: ', pic_name)
#                 print('sys_path: ', sys_path)
                       
                img_full_path = sys_path + '/' + pic_name
                
                pr(img_full_path)
        
                dst = shutil.copy2(root + '/' + str(f), img_full_path)
#                 pr(dst)
                 
                img_dict = {}
                img_dict['lib'] = library_name
                img_dict['stack'] = str(time_stamp)
                img_dict['batch'] = batch_num
                img_dict['plate'] = s_plate
                 
                views_util.writeExiv(img_dict, img_full_path)
                 
                browser_path = inner_path  + '/' +  pic_name
                 
                 
                 
                p = YeastPlate_Model.objects.filter(scheme__index = int(s_plate))
                 
                if len(p) > 0:
            
                    views_util.analyseInBackground(stack.pk, s_plate, batch_num, browser_path, img_full_path, foreground, os_type, out_con=out_con)
                     
                else:
                    print(img_full_path + " does not correspond to a plate in this library scheme")
                
    
    except Exception:
        print('exception: ', sys.exc_info)
        traceback.print_exc()
    
    

def C():

    path = "/cs/wetlab/Ayelet/Libraries/KO_Shai/KO_Shai_Images/KO_Shai22.1.12"
    
    for root, dirs, files in os.walk(path):
    #         print('')
    #         print("Current directory: " + root)
    #         print("Sub directories: " + str(dirs))
    #         print("Files: " + str(files))
            
        for f in files: 
             
            semantic = str(f)
            pr(semantic)

            if str(f)[0] == '.':
                
                pr('hidden directory')
                continue
    
    
def chrono_stack_origin():

    '''
    '''

    stacks = YeastPlateStack_Model.objects.filter(library__name='KO_Shai').order_by('-time_stamp')

    stacks_num = len(stacks)

    for i in range(stacks_num):

        stack = stacks[i]
        print(stack.__str__())
        print('stack.parent: ', stack.parent)

        if(i < len(stacks)-1):

            stack.parent = stacks[i+1]
            stack.save()


    for i in range(stacks_num):

        stack = stacks[i]
        print(stack.__str__())
        print('stack.parent: ', stack.parent)



def view_origin():

    '''
    '''

    stacks = YeastPlateStack_Model.objects.filter(library__name='KO_Shai').order_by('-time_stamp')

    stacks_num = len(stacks)

    for i in range(stacks_num):

        stack = stacks[i]
        print(stack.__str__())
        print('stack.parent: ', stack.parent)


def sn_sc(snapshot_pk=40):

     try:
        con = psycopg2.connect(host = 'cab-27', database=settings.DB_NAME)
        cur = con.cursor()

        command = 'SELECT id FROM yeast_libraries_platelocus_model WHERE scheme_id = (SELECT scheme_id FROM snapshot_scheme WHERE snapshot_id = ' + str(snapshot_pk) + ') AND row = ' +\
                  "'E'" + \
                  ' AND "column" = 3;'

        cur.execute(command)
        # print('cur.fetchone(): ', cur.fetchone())

        print('cur.fetchone()[0]: ', cur.fetchone()[0])

     except Exception:
        print('exception: ', sys.exc_info)
        traceback.print_exc()


     finally:
        if con:
            con.close()
    

def Q():

    try:
        con = psycopg2.connect(host = 'cab-27', database=settings.DB_NAME)
        cur = con.cursor()

        command = 'SELECT id FROM yeast_libraries_platelocus_model WHERE scheme_id = 46 AND row = ' + "'G'" + ' AND "column" = 9'

        cur.execute(command)

        print('type(cur.fetchone()): ', type(cur.fetchone()))

        # print('cur.fetchone()[0]: ', cur.fetchone()[0])

    except Exception:
        print('exception: ', sys.exc_info)
        traceback.print_exc()


    finally:
        if con:
            con.close()

