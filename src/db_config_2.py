import os, sys, traceback

from yeast_libraries.models import StorageLocation_Model, YeastStrain_Model, YeastLibrary_Model, PlateFormat_Model, PlateLocus_Model, PlateScheme_Model, YeastPlateStack_Model,\
    YeastPlate_Model
from suppliers.models import Source_Model
from mediums.models import Compound_Model, Batch_Model

from datetime import datetime

from lab import settings

from excels.lib_parser import LibraryParser

print('kalipski')


try:      
    library = YeastLibrary_Model.objects.filter(name='Haploid_KO_Maya_new')
    
    print('type(library): ', type(library))
    
    if library.count() > 0:
        print('library found: ', library[0].__str__())
    else:
        print('library missing') 

        data = os.path.join(settings.BASE_DIR, 'yeast_libraries/static/yeast_libraries/xls/Haploid_KO_Maya_new.xls')
        
        libraryParcer = LibraryParser()
            
        libraryParcer.libraryExcelParser(data)
        
        
        
    library = YeastLibrary_Model.objects.filter(name='KOShai_yldb_ver')
    
    print('type(library): ', type(library))
    
    if library.count() > 0:
        print('library found: ', library[0].__str__())
    else:
        print('library missing') 

        data = os.path.join(settings.BASE_DIR, 'yeast_libraries/static/yeast_libraries/xls/KOShai_yldb_ver.xls')
        
        libraryParcer = LibraryParser()
            
        libraryParcer.libraryExcelParser(data)
        
        

    library = YeastLibrary_Model.objects.filter(name='Magicdip-yldb-version')
    
    print('type(library): ', type(library))
    
    if library.count() > 0:
        print('library found: ', library[0].__str__())
    else:
        print('library missing') 

        data = os.path.join(settings.BASE_DIR, 'yeast_libraries/static/yeast_libraries/xls/Magicdip-yldb-version.xls')
        
        libraryParcer = LibraryParser()
            
        libraryParcer.libraryExcelParser(data, personal_name='everyone')
       
        #Magicdip-yldb-version.xls
          
     
except Exception:
    print(sys.exc_info())
    traceback.print_exc()