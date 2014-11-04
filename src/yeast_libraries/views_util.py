
import os, multiprocessing, sys, traceback, json, pwd, grp
import psycopg2

from cmd_utils.exiv2 import Exiv2
from datetime import datetime



from lab import settings
# from image_analysis.image_processor import ImageAnalysisControler
from yeast_libraries.models import YeastPlateStack_Model, YeastPlate_Model,\
    SnapshotBatch_Model, PlateSnapshot_Model, SnapshotProcess_Model
from django.utils.termcolors import foreground
from lab_util.util import pr


ALL_NICKNAMES = 'ALL_NICKNAMES';
COMMON_USER = 'everyone'


def validateStackDirs(library_name, time_stamp_as_string):

    try:
        inner_path = os.path.join(library_name, 'copy', time_stamp_as_string[:-6])
         #     print('inner_path: ', inner_path)
#         print('settings.PLATE_IMAGE_ROOT: ', settings.PLATE_IMAGE_ROOT)
        sys_path = os.path.join(settings.PLATE_IMAGE_ROOT, inner_path)
#         sys_path = os.path.join('/cs/wetlab/yeast_library_images', inner_path)   



        if not os.path.exists(sys_path):

            print('sys_path: ', sys_path)
            uid = pwd.getpwnam('gideonbar').pw_uid
            gid = grp.getgrnam('yeast_im').gr_gid

            split_path = sys_path.split('/')

            tmpath = ''

            for s in split_path:

                tmpath = '/'.join([tmpath, s])

                print('tmpath: ', tmpath)

                if not os.path.exists(tmpath):

                    os.mkdir(tmpath)
                    print('boogy')
                    os.chmod(tmpath, 0o775)
                    os.chown(tmpath, uid, gid)



        else:
               
            for root, dirs, files in os.walk(sys_path):
                print('')
                print("Current directory: " + root)
#                 print("Sub directories: " + str(dirs))
#                 print("Files: " + str(files))
            #this is to save versions of images
#                 for f in files: 
#                      
#                     semantic = str(f)[0:-5].split('_')
#                      
#                     s_plate_num = int(semantic[1])
#                     s_version = int(semantic[3])
                                             
    except Exception:        
        print(sys.exc_info())
        print('just printed exception')
        return 'error'

    return [sys_path, inner_path]


def writeExiv(img_dict, img_full_path):
    
    s = str(img_dict).replace(', ', ',').replace(': ', ':')
#         print('img_dict to exiv: ', s)
    
    exiv2 = Exiv2()
    exiv2.addComment(img_full_path, s)
    meta_data = exiv2.getComment(img_full_path)
    
#     print('processImage:', datetime.now(), '    finished meta_data:', meta_data)
    print('just added snapshot processImage:', datetime.now(), '    finished meta_data:', meta_data)


def analyseInBackground(stack_pk, plate_num, batch_num, browser_path, img_full_path, foreground = None):
    
    try:
        stack = YeastPlateStack_Model.objects.get(pk = stack_pk)
        plate = YeastPlate_Model.objects.get(stack = stack, scheme__index = plate_num)
        
    #             print('type(plate): ', type(plate))
    #             print('plate.__str__(): ', plate.__str__())
        
        snapshot_batch, created = SnapshotBatch_Model.objects.get_or_create(plate = plate, index = batch_num)
        
    #             print('str(snapshot_batch.pk): ', str(snapshot_batch.pk))
    #             
    #             if created:
    #                 print('just created snapshot_batch #', batch_num, 'for', plate.__str__())
    #             else:
    #                 print('just retrieved snapshot_batch #', batch_num, 'for', plate.__str__())
        
        
        snapshot, created = PlateSnapshot_Model.objects.get_or_create(batch = snapshot_batch, image_path = browser_path)
        
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
    
    except Exception:
        print('exception: ', sys.exc_info)
        traceback.print_exc()
    #        
    
    process_table_name = snapshot_process._meta.db_table
    #         print('snapshot_process._meta.db_table: ', process_table_name) 

    # imageAnalysisControler = ImageAnalysisControler()
    
    
    if foreground:
        
        pr('foreground operation')
        
        # imageAnalysisControler.processImage(settings.BASE_DIR, settings.PLATE_IMAGE_ROOT, img_full_path, snapshot.pk, process_pk, settings.DB_NAME, process_table_name)
        
    else:


        try:
        
            # pr('multiprocessing operation')
            #
            # process = multiprocessing.Process(target=ImageAnalysisControler.processImage, args=(imageAnalysisControler, settings.BASE_DIR, settings.PLATE_IMAGE_ROOT, img_full_path, snapshot.pk, process_pk, settings.DB_NAME, process_table_name))
            # process.start()

            pr('slurm operation')

            # d = {"action": "run", "type": "dnaseq", "data": {"command":"image_processor.py",
            d = {"action": "run", "type": "wetlab", "data": {"command":"image_processor.py",
                    "args": [settings.BASE_DIR, settings.PLATE_IMAGE_ROOT, img_full_path, snapshot.pk, process_pk, settings.DB_NAME, process_table_name]}}

            j = json.dumps(d)
            print('j: ', j)

            con = psycopg2.connect(host = 'pghost', database='ribs', user='gideonbar')
            cur = con.cursor()

            column_names = '(' + ', '.join(['info']) + ')'
            values = '(' + "'" + j + "'" + ')'
            command = 'INSERT INTO slurm.wetlab ' + column_names + ' VALUES ' + values + ' RETURNING id'

            # command = 'INSERT INTO slurm.requests ' + column_names + ' VALUES ' + values + ' RETURNING id'

            cur.execute(command)
            slurm_id = cur.fetchone()[0]
            print('slurm_id: ', slurm_id)
            con.commit()

        except Exception:
            print('exception: ', sys.exc_info)
            traceback.print_exc()


        finally:

            if con:
                con.close()
    
    return [snapshot, process_pk]
    
    