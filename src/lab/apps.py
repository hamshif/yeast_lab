import sys, traceback
from django.apps import AppConfig

from lab import settings
import psycopg2




class LabConfig(AppConfig):

    name = 'lab'
    verbose_name = "WETLAB site"

    def ready(self):

        print('wikelleloo')

        try:

            con = psycopg2.connect(host = 'cab-27', database=settings.DB_NAME)
            cur = con.cursor()

            cur.execute("CREATE OR REPLACE VIEW snapshot_scheme AS SELECT yeast_libraries_platesnapshot_model.id AS snapshot_id, yeast_libraries_snapshotbatch_model.id AS batch_id, yeast_libraries_yeastplate_model.id AS plate_id, yeast_libraries_platescheme_model.id AS scheme_id FROM yeast_libraries_platesnapshot_model JOIN yeast_libraries_snapshotbatch_model ON yeast_libraries_platesnapshot_model.batch_id = yeast_libraries_snapshotbatch_model.id JOIN yeast_libraries_yeastplate_model ON yeast_libraries_snapshotbatch_model.plate_id = yeast_libraries_yeastplate_model.id JOIN yeast_libraries_platescheme_model ON yeast_libraries_yeastplate_model.scheme_id = yeast_libraries_platescheme_model.id;")

            con.commit()

            print('granted permissions')

        except Exception:

            print('exception: ', sys.exc_info)
            traceback.print_exc()

        finally:

            if con:
                con.close()

