
#!/usr/bin/env python3.3
#SBATCH -o /cs/system/gideonbar/tmp/output-%j
#SBATCH -e /cs/system/gideonbar/tmp/error-%j
#SBATCH -c 8
#SBATCH --mem 20000

import sys

ar = sys.argv

for a in ar:
    print('arg: ', a)


print('no more args')



import traceback, json, subprocess

import psycopg2

from datetime import datetime



class ImageAnalysisControler:


    def processImage(self, base_dir, plate_image_root, img_full_path, snapshot_pk, process_pk, db_name, process_table_name):

        print('yeepee')
#         print('')
#         print('I think I just closed th db connection connection')
#         print('')


#         print('processImage:', datetime.now())
#         print('process_pk: ', process_pk)
        sys.stdout.flush()

        try:
            con = psycopg2.connect(host = 'cab-27', database=db_name, user='gideonbar')
            cur = con.cursor()

            cur.execute('SELECT status FROM ' + process_table_name + ' WHERE id = ' + str(process_pk))
#             print('cur.fetchone(): ', cur.fetchone())

            imageAnalysisControler = ImageAnalysisControler()
#
            processed_image_path = img_full_path[:-5] + '_p.jpg'

            global grid

#             print('process image: getting analysis')

            grid = imageAnalysisControler.analyzeYeastPlateImage(base_dir, img_full_path, processed_image_path)


            delete_previous_analysis = "DELETE FROM yeast_libraries_locusanalysis_model WHERE snapshot_id = " + str(snapshot_pk)
            cur.execute(delete_previous_analysis)
            con.commit()
#             print('just deleted old analysis loci if they existed')

            relative_path = processed_image_path.replace(plate_image_root + '/', '')

            cur.execute("UPDATE yeast_libraries_platesnapshot_model SET processed_image_path = '" + relative_path + "' WHERE id = " + str(snapshot_pk))
            con.commit()


            sys.stdout.flush()

            if grid == 'failed':

                print('process image: failed')
                grid = imageAnalysisControler.analyzeYeastPlateImage(base_dir, base_dir + '/image_analysis/static/image_analysis/384_0001.jpg', processed_image_path)
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

#                     print('idd: ', idd, '  snapshot_pk: ', snapshot_pk)



            cur.execute("UPDATE " + process_table_name + " SET status = 'complete' WHERE id = " + str(process_pk))
            con.commit()


            sys.stdout.flush()

            cur.execute('SELECT status FROM ' + process_table_name + ' WHERE id = ' + str(process_pk))
#             print("cur.execute('SELECT status FROM ' + process_table_name + ' WHERE id = ' + str(process_pk))")
#             print('cur.fetchone(): ', cur.fetchone())

        except Exception:
            print('exception: ', sys.exc_info)
            traceback.print_exc()

            try:
                if con:
                    con.close()
                con = psycopg2.connect(host = 'cab-27', database=db_name, user='gideonbar')
                cur = con.cursor()
                cur.execute("UPDATE " + process_table_name + " SET status = 'failed' WHERE id = " + str(process_pk))
                con.commit()
                print('failed default transpired')

            except Exception:
                print('exception: ', sys.exc_info)
                traceback.print_exc()

        finally:
            if con:
                con.close()



        print('finished processing image')
        sys.stdout.flush()



    def analyzeYeastPlateImage(self, base_dir, image_path, processed_path):

#
#         print(' ')
#         print('analyzeYeastPlateImage')
        print('img_path: ' + image_path)
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

            sys.stdout.flush()


        print('exiting analyzeYeastPlateImage')

        return j




    
    


