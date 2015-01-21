#!/usr/bin/env python3.4
#S#BATCH -o /cs/system/gideonbar/tmp_wet/output-%j
#S#BATCH -e /cs/system/gideonbar/tmp_wet/error-%j
#SBATCH -o /dev/null
#SBATCH -e /dev/null
#SBATCH -c 2
#SBATCH --mem 1000
#SBATCH --time 0:2:0

import sys, os

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
                    self.saveGrid(grid, con, cur, snapshot_pk)
                    status = 'complete'

                else:

                    status = 'failed_to_analyze'
                    cur.execute("UPDATE yeast_libraries_platesnapshot_model SET processed_image_path = '" + status + "' WHERE id = " + str(snapshot_pk))
                    con.commit()

            else:

                print('process image: got analysis')
                print('')
                self.saveGrid(grid, con, cur, snapshot_pk)
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

        full_path_c_script = os.path.join(base_dir, "Process")

        if(os_type == 'FreeBSD'):
            full_path_c_script = full_path_c_script + '.fbsd'

        print('full_path_c_script: ', full_path_c_script)

        p = subprocess.Popen([full_path_c_script, '-i', processed_path, image_path], stdout=subprocess.PIPE)
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



    def saveGrid(self, grid, con, cur, snapshot_id):

        print('snapshot_id: ', snapshot_id)


        command = 'SELECT scheme_id FROM snapshot_scheme WHERE snapshot_id = ' + str(snapshot_id)

        cur.execute(command)
        # print('cur.fetchone(): ', cur.fetchone())

        scheme_id = cur.fetchone()[0]

        print('scheme_id: ', scheme_id)

        column_names = '(' + ', '.join(['area_scaled', 'is_empty', '"column"', 'row', 'ratio', 'center_x', 'center_y', 'snapshot_id', 'locus_id']) + ')'

        print('column_names: ', column_names)


        for cell in grid['grid']:
            # find corresponding locus

            column = str(cell['column'] + 1)
            row = chr(cell['row'] + ord('A'))


            print('column: ', column, '   row: ', row)

            command = 'SELECT id FROM yeast_libraries_platelocus_model WHERE scheme_id = ' + str(scheme_id) + ' AND row = ' + "'" + row + "'" + ' AND "column" = ' + column + ';'
            print('command: ', command)


            cur.execute(command)

            res = cur.fetchone()

            if res is None:

                locus_id = 'NULL'

            else:

                locus_id = str(res[0])


            values = '(' + ', '.join([str(cell['area_scaled']), str(cell['is_empty']), str(cell['column']), str(cell['row']), str(cell['ratio']), str(cell['center_x']), str(cell['center_y']), str(snapshot_pk), locus_id]) + ')'

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

    
    
def test():

    try:

        from lab import settings

        base_dir = settings.BASE_DIR
        plate_image_root = settings.PLATE_IMAGE_ROOT
        img_full_path = "/cs/wetlab/dev1_yeast_library_images/Hismut_yldb_version/copy/2015-01-03%s13:00:00/plate_1_batch_1_v_1.jpeg"
        snapshot_pk=2477
        process_pk=2477
        db_name = settings.DB_NAME
        process_table_name = "yeast_libraries_snapshotprocess_model"
        analyze_default = False


        print('base_dir: ', base_dir)
        print('plate_image_root: ', plate_image_root)
        print('img_full_path: ', img_full_path)


        imageAnalysisControler = ImageAnalysisControler()

        imageAnalysisControler.processImage(base_dir, plate_image_root, img_full_path, snapshot_pk, process_pk, db_name, process_table_name, analyze_default=analyze_default)

    except Exception:
        print('exception: ', sys.exc_info)
        traceback.print_exc()
