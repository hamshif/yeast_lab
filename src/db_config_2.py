import os, sys, traceback

from yeast_libraries.models import StorageLocation_Model, YeastStrain_Model, YeastLibrary_Model, PlateFormat_Model, PlateLocus_Model, PlateScheme_Model, YeastPlateStack_Model,\
    YeastPlate_Model
from suppliers.models import Source_Model
from mediums.models import Compound_Model, Batch_Model

from datetime import datetime

from lab import settings

from excels.lib_parser import LibraryParser

print('kalipski')

'Haploid_KO_Maya'




def regAllLibs():

    libs = ['His_Mut', 'GFP', 'Haploid_KO_Maya', 'KO_Shai', 'Magic_Dip']

    for l in libs:

        autoRegisterLib(library_name=l)


def autoRegisterLib(library_name='His_Mut'):

    try:
        library = YeastLibrary_Model.objects.filter(name=library_name)

        if library.count() > 0:
            print('library found: ', library[0].__str__())
        else:
            print('library missing')

            data = os.path.join(settings.BASE_DIR, 'yeast_libraries/static/yeast_libraries/xls/' + library_name +'.xls')

            libraryParcer = LibraryParser()

            libraryParcer.libraryExcelParser(data, personal_name='everyone')

    except Exception:
        print(sys.exc_info())
        traceback.print_exc()