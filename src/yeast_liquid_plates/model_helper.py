import sys, traceback
from yeast_liquid_plates.models import SpectrometerExperiment_Model,\
    LiquidYeastPlate_Model
import yeast_libraries
from yeast_libraries.models import YeastPlateStack_Model, YeastLibrary_Model

class LiquidExperimentHelper():
    """
    """
    
    def byPlate(self, plate_pk):
        
        r = []
        
        try:
            
            experiments = SpectrometerExperiment_Model.objects.filter(plate__pk = plate_pk)    
            
            for e in experiments:
                
                r.append({'name': e.__str__(), 'id': e.pk, 'plate_id': e.plate.yeast_plate.pk})
        
        except Exception: 
            
            print('exception: ', sys.exc_info)
            traceback.print_exc()   
        
        print('LiquidExperimentHelper.byPlate: ', r)
        return r
        
    
    def byCopy(self, copy_pk):
        
        r = {}
        
        try:
            
            plates = LiquidYeastPlate_Model.objects.filter(yeast_plate__stack__pk = copy_pk)    
            
            for p in plates:
                
                r[p.pk] = self.byPlate(p.pk)
        
        except Exception: 
            
            print('exception: ', sys.exc_info)
            traceback.print_exc()   
        
        print('LiquidExperimentHelper.byCopy: ', r)
        return r
      
        
    def byLib(self, lib_pk):
        
        r = {}
        
        try:
            
            copies = YeastPlateStack_Model.objects.filter(library__pk = lib_pk)    
            
            for c in copies:
                
                r[c.pk] = self.byCopy(c.pk)
        
        except Exception: 
            
            print('exception: ', sys.exc_info)
            traceback.print_exc()   
        
        print('LiquidExperimentHelper.byLib: ', r)
        return r
    
    
    def  byUserLibs(self, user):
        
        r = {}
        
        try:
            
            libs = YeastLibrary_Model.objects.filter(personal_name = user)
    
            r = {}
            
            for l in libs:
                
                r[l.pk] = self.byLib(l.pk)
        
        except Exception: 
            
            print('exception: ', sys.exc_info)
            traceback.print_exc()   
        
        print('LiquidExperimentHelper.byUserLibs: ', r)
        return r
    
    