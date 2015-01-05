

import yeast_libraries.models as models

import sys, traceback, json, subprocess

import psycopg2

from lab import settings
import os

class ImageAnalysisControler:

    def analyzeYeastPlateImage(self, base_dir, image_path, processed_path):
         
#          
#         print(' ') 
#         print('analyzeYeastPlateImage') 
#         print('img_path: ', image_path) 
#         print('processed path: ', processed_path) 
        p = subprocess.Popen([base_dir + "/image_analysis/Process", '-i', processed_path, image_path], stdout=subprocess.PIPE)
#         tthe lines bellow are functions that hange the images don't touch for now
#         p = subprocess.Popen(["Process", '-C', image_path, 'plates/384_0002.jpg'], stdout=subprocess.PIPE)
#         p = subprocess.Popen(["Process", '-i', image_path, 'plates/384_0002.jpg'], stdout=subprocess.PIPE)

        out, err = p.communicate()
#         print(' ')
        
        a = out.decode()
        
#         print('output from image recognition software: ', a)
        
        try:
            j = json.loads(a)
            
        except Exception:
            print('exception: ', sys.exc_info)
            traceback.print_exc()
            
#             print('analyzeYeastPlateImage() failed to process image')
            return 'failed'
         
         
        for key in j:

            value = j[key]
            
            if isinstance(value, type([])):
                
                print('key: ', key)
                
                for v in value:
                    
                    print(v)
#                     if v['is_empty']:
#                         print("is empty")
#                     else:
#                         print(v)
                 
            else:
                print('key: ', key, ' value: ', j[key])
        

        return j
        

    def processImage(self, base_dir, plate_image_root, img_full_path, snapshot_pk, db_name):
        
        
#         print('processImage1:', datetime.now())
#         print('process_pk: ', process_pk)
        sys.stdout.flush()
        
        try:
            con = psycopg2.connect(host = 'cab-27', database=db_name) 
            cur = con.cursor() 
            
#             cur.execute('SELECT status FROM ' + process_table_name + ' WHERE id = ' + str(process_pk))
#             print('cur.fetchone(): ', cur.fetchone())
#             
            processed_image_path = img_full_path[:-5] + '_p.jpg'
             
            global grid
              
#             print('process image: getting analysis')
             
            grid = self.analyzeYeastPlateImage(base_dir, img_full_path, processed_image_path)
            
            
            delete_previous_analysis = "DELETE FROM yeast_libraries_locusanalysis_model WHERE snapshot_id = " + str(snapshot_pk)
            cur.execute(delete_previous_analysis)
            con.commit()
#             print('just deleted old analysis loci if they existed')
            
            relative_path = processed_image_path.replace(plate_image_root + '/', '')
                 
            cur.execute("UPDATE yeast_libraries_platesnapshot_model SET processed_image_path = '" + relative_path + "' WHERE id = " + str(snapshot_pk))
            con.commit()
            
            
            sys.stdout.flush()
            
            if grid == 'failed':
            
#                 print('process image: failed')
                grid = self.analyzeYeastPlateImage(base_dir, base_dir + '/image_analysis/static/image_analysis/384_0001.jpg', processed_image_path)
#                 print('for debug analyzing default image')
#                 cur.execute("UPDATE " + process_table_name + " SET status = 'failed' WHERE id = " + str(process_pk))
#                 con.commit()  
#  
#             else:
                 
#                 print('process image: got analysis')

                
#                 print('')
                
                for cell in grid['grid']:
                    
                    column_names = '(' + ', '.join(['area_scaled', 'is_empty', '"column"', 'row', 'ratio', 'center_x', 'center_y', 'snapshot_id']) + ')'
                    #print('column_names: ', column_names)
                    values = '(' + ', '.join([str(cell['area_scaled']), str(cell['is_empty']), str(cell['column']), str(cell['row']), str(cell['ratio']), str(cell['center_x']), str(cell['center_y']), str(snapshot_pk)]) + ')'
                    
                    command = 'INSERT INTO yeast_libraries_locusanalysis_model ' + column_names + ' VALUES ' + values + ' RETURNING id'
    #                 print('command: ', command)
                    
                    cur.execute(command)
                    idd = cur.fetchone()[0]
                    con.commit()
                    
                    print('idd: ', idd, '  snapshot_pk: ', snapshot_pk)



#                 cur.execute("UPDATE " + process_table_name + " SET status = 'complete' WHERE id = " + str(process_pk))
#                 con.commit()                
     
            sys.stdout.flush()


 
            
#             cur.execute('SELECT status FROM ' + process_table_name + ' WHERE id = ' + str(process_pk))
#             print("cur.execute('SELECT status FROM ' + process_table_name + ' WHERE id = ' + str(process_pk))")
#             print('cur.fetchone(): ', cur.fetchone())

            
        except Exception:
            print('exception: ', sys.exc_info)
            traceback.print_exc()
            
            try:
                if con:
                    con.close()
#                 con = psycopg2.connect(host = 'cab-27', database=db_name) 
#                 cur = con.cursor() 
#                 cur.execute("UPDATE " + process_table_name + " SET status = 'failed' WHERE id = " + str(process_pk))
#                 con.commit()
#                 print('failed default transpired')
                
            except Exception:
                print('exception: ', sys.exc_info)
                traceback.print_exc()
            
        finally:
            if con:
                con.close()






processUtil = ImageAnalysisControler()
lios = models.PlateSnapshot_Model.objects.all()

base_dir = settings.BASE_DIR
plate_image_root = settings.PLATE_IMAGE_ROOT
db_name = settings.DB_NAME


for sn in lios:
    
    img_full_path = os.path.join(plate_image_root, sn.image_path)
    
    processUtil.processImage(base_dir, plate_image_root, img_full_path, sn.pk, db_name)
