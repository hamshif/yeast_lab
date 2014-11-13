#!/cs/system/gideonbar/dev/workspace/lab/venv_lab_linux/bin/python3.3
#SBATCH -o /cs/system/gideonbar/tmp_wet/output-%j
#SBATCH -e /cs/system/gideonbar/tmp_wet/error-%j
#SBATCH -c 2
#SBATCH --mem 1000
#SBATCH --time 0:2:0

import sys

ar = sys.argv

for a in ar:
    print('arg: ', a)


print('no more args')



import traceback, json, subprocess

import psycopg2

from datetime import datetime



class ImageAnalysisControler:


    def processImage(self, base_dir, plate_image_root, img_full_path, snapshot_pk, process_pk, db_name, process_table_name, os_type = 'linux', analyze_default=False):

        try:
            con = psycopg2.connect(host = 'cab-27', database=db_name)
            cur = con.cursor()

            print('analyze_default: ', analyze_default)

            cur.execute('SELECT status FROM ' + process_table_name + ' WHERE id = ' + str(process_pk))
#             print('cur.fetchone(): ', cur.fetchone())

            imageAnalysisControler = ImageAnalysisControler()
#
            processed_image_path = img_full_path[:-5] + '_p.jpg'

            print('processed_image_path: ',  processed_image_path)

            global grid

#             print('process image: getting analysis')

            grid = imageAnalysisControler.analyzeYeastPlateImage(base_dir, img_full_path, processed_image_path, os_type)


            delete_previous_analysis = "DELETE FROM yeast_libraries_locusanalysis_model WHERE snapshot_id = " + str(snapshot_pk)
            cur.execute(delete_previous_analysis)
            con.commit()
#             print('just deleted old analysis loci if they existed')

            relative_path = processed_image_path.replace(plate_image_root + '/', '')

            print('relative_path: ',  relative_path)

            cur.execute("UPDATE yeast_libraries_platesnapshot_model SET processed_image_path = '" + relative_path + "' WHERE id = " + str(snapshot_pk))
            con.commit()


            status = 'failed'

            if grid == 'failed':

                print('process image: failed       analyze_default: ', analyze_default)

                if analyze_default:

                    print('type(analyze_default: ', type(analyze_default))


                    grid = imageAnalysisControler.analyzeYeastPlateImage(base_dir, base_dir + '/image_analysis/static/image_analysis/384_0001.jpg', processed_image_path, os_type)
                    print('for debug analyzing default image')
                    self.saveGrid(self, grid, con, cur)
                    status = 'complete'

                else:

                    status = 'failed_to_analyze'
                    cur.execute("UPDATE yeast_libraries_platesnapshot_model SET processed_image_path = '" + status + "' WHERE id = " + str(snapshot_pk))
                    con.commit()

            else:

                print('process image: got analysis')
                print('')
                self.saveGrid(self, grid, con, cur)
                status = 'complete'


            cur.execute("UPDATE " + process_table_name + " SET status = '" + status + "' WHERE id = " + str(process_pk))
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
                con = psycopg2.connect(host = 'cab-27', database=db_name)
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



    def analyzeYeastPlateImage(self, base_dir, image_path, processed_path, os_type='linux'):

#
#         print(' ')
#         print('analyzeYeastPlateImage')
        print('img_path: ' + image_path)
        print('processed path: ', processed_path)

        path_to_c_software = "/cs/system/gideonbar/dev/workspace/lab/src/image_analysis/Process"

        if(os_type == 'FreeBSD'):
            path_to_c_software = "/cs/system/gideonbar/dev/workspace/lab/src/image_analysis/Process.fbsd"

        print('path_to_c_software: ', path_to_c_software)

        p = subprocess.Popen([path_to_c_software, '-i', processed_path, image_path], stdout=subprocess.PIPE)
        #for running on same machine ass app p = subprocess.Popen([base_dir + "/image_analysis/Process", '-i', processed_path, image_path], stdout=subprocess.PIPE)
#         tthe lines bellow are functions that hange the images don't touch for now
#         p = subprocess.Popen(["Process", '-C', image_path, 'plates/384_0002.jpg'], stdout=subprocess.PIPE)
#         p = subprocess.Popen(["Process", '-i', image_path, 'plates/384_0002.jpg'], stdout=subprocess.PIPE)

        # p.wait(timeout=None)
        #
        out, err = p.communicate()



        a = out.decode()

        print('output from image recognition software: ')
        print(a)

        try:
            j = json.loads(a)

        except Exception:
            print('exception: ', sys.exc_info)
            traceback.print_exc()

            print('analyzeYeastPlateImage() failed to process image')
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



    def saveGrid(self, grid, con, cur):

        for cell in grid['grid']:

            column_names = '(' + ', '.join(['area_scaled', 'is_empty', '"column"', 'row', 'ratio', 'center_x', 'center_y', 'snapshot_id']) + ')'
            #print('column_names: ', column_names)
            values = '(' + ', '.join([str(cell['area_scaled']), str(cell['is_empty']), str(cell['column']), str(cell['row']), str(cell['ratio']), str(cell['center_x']), str(cell['center_y']), str(snapshot_pk)]) + ')'

            command = 'INSERT INTO yeast_libraries_locusanalysis_model ' + column_names + ' VALUES ' + values + ' RETURNING id'
#                 print('command: ', command)

            cur.execute(command)
            idd = cur.fetchone()[0]
            con.commit()

            status = 'complete'





if len(ar) > 8:

    try:

        base_dir = ar[1]
        plate_image_root = ar[2]
        img_full_path = ar[3]
        snapshot_pk = ar[4]
        process_pk = ar[5]
        db_name = ar[6]
        process_table_name = ar[7]
        analyze_default = ar[8]

        if analyze_default == 'False':

            analyze_default = False

        else:

            analyze_default = True

        print('base_dir: ', base_dir)
        print('plate_image_root: ', plate_image_root)
        print('img_full_path: ', img_full_path)


        imageAnalysisControler = ImageAnalysisControler()

        imageAnalysisControler.processImage(base_dir, plate_image_root, img_full_path, snapshot_pk, process_pk, db_name, process_table_name, analyze_default=analyze_default)

    except Exception:
        print('exception: ', sys.exc_info)
        traceback.print_exc()

    
    


