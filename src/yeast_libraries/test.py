import sys, traceback
from yeast_libraries.models import SnapshotBatch_Model

from yeast_libraries import db_manager


def deleteSnapshots(batch_pk):
    
    try:
        b = SnapshotBatch_Model.objects.get(pk=batch_pk)
        db_manager.deleteSnapshots(b)
    
    except Exception:
        print('exception: ', sys.exc_info)
        traceback.print_exc()