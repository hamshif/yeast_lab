import os, sys, traceback

from yeast_libraries.models import StorageLocation_Model, YeastStrain_Model, YeastLibrary_Model, PlateFormat_Model, PlateLocus_Model, PlateScheme_Model, YeastPlateStack_Model,\
    YeastPlate_Model
from suppliers.models import Source_Model
from mediums.models import ChemicalCompound_Model, Compound_Model, Batch_Model

from datetime import datetime

from lab import settings

from excels.lib_parser import LibraryParser


try:
    
    time_stamp = datetime(year = 2000, day = 3, month = 7, hour = 13, minute = 40)
    
    
    plate_format, created = PlateFormat_Model.objects.get_or_create(width_loci=16, length_loci=8)
    if created:
        print(plate_format.__str__(), 'was created')
        plate_format.save()
    else:
        print(plate_format.__str__(), 'was retrieved')
        
    plate_format, created = PlateFormat_Model.objects.get_or_create(width_loci=24, length_loci=16)
    if created:
        print(plate_format.__str__(), 'was created')
        plate_format.save()
    else:
        print(plate_format.__str__(), 'was retrieved')
        
    plate_format, created = PlateFormat_Model.objects.get_or_create(width_loci=48, length_loci=32)
    if created:
        print(plate_format.__str__(), 'was created')
        plate_format.save()
    else:
        print(plate_format.__str__(), 'was retrieved')    
    
    
    location, created = StorageLocation_Model.objects.get_or_create(location='Freezer')
     
    if created:
        print('Freezer location created')
        location.save();
    else:
        print('Freezer location retrieved')
         
    location, created = StorageLocation_Model.objects.get_or_create(location='Refrigerator')
     
    if created:
        print('Refrigerator location created')
        location.save();
    else:
        print('Refrigerator location retrieved')
    
    supplier, created = Source_Model.objects.get_or_create(name='smee', description='Swashbuckler of ill repute')
    
    if created:
        print('supplier created')
        supplier.save();
    else:
        print('supplier retrieved')
    
    
    
    chemical_compound, created = ChemicalCompound_Model.objects.get_or_create(name = 'Ager', chemical_description = 'extract')
    
    if created:
        print('chemical_compound created')
        chemical_compound.save();
    else:
        print('chemical_compound retrieved')
        
    compound, created = Compound_Model.objects.get_or_create(chemical = chemical_compound, quantity_in_miligrams = 3000, time_stamp = time_stamp)
    
    if created:
        print('compound created')
        compound.save();
    else:
        print('compound retrieved')    
        
        
        
        
       
    medium, created = Batch_Model.objects.get_or_create(type = 'Plain Ager', time_stamp = time_stamp, source = 'crazy harry')
    medium.compounds.add(compound)
    
    if created:
        print('compound created')
        medium.save();
    else:
        print('compound retrieved')  

except Exception:
    print(sys.exc_info())
    traceback.print_exc()