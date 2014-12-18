
from yeast_libraries.models import YeastPlateStack_Model


def stacks(library_name="Hismut_yldb_version"):

    ss = YeastPlateStack_Model.objects.filter(library__name=library_name)

    for s in ss: print(s.__str__(), ' ', s.is_liquid)



def del_stacks(library_name="Hismut_yldb_version"):

    ss = YeastPlateStack_Model.objects.filter(library__name=library_name)

    for s in ss:

        print(s.__str__(), ' ', s.is_liquid)
        s.delete()


