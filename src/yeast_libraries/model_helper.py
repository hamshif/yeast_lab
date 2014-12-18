from yeast_libraries.models import YeastPlate_Model , YeastPlateStack_Model,\
    SnapshotBatch_Model, PlateSnapshot_Model, YeastLibrary_Model
from yeast_liquid_plates.models import LiquidYeastPlate_Model
from yeast_libraries.views_util import ALL_NICKNAMES


class LibraryHelper():
    """
    """
    
    def __init__(self):
        
        self.copyHelper = CopyHelper()
    
    
    def getBareDict(self, lib, is_liquid):
        
        bare = {}
        
        bare['pk'] = lib.pk
        bare['name'] = lib.name
        
        bare_stacks = {}
        
        for b in YeastPlateStack_Model.objects.filter(library__pk = lib.pk, is_liquid = is_liquid).order_by('time_stamp'):
            
            bare_stacks[b.__str__()] = self.copyHelper.getBareDict(b)
        
        bare['stacks'] = bare_stacks        
        
        return bare
    
    
    def getPlateMaps(self, nicknames, is_liquid):
        """
        """
        
#         print('     is_liquid: ', is_liquid)

        lib_order = []
        plate_maps = {}
        
        if ALL_NICKNAMES in nicknames:
            
            libraries = YeastLibrary_Model.objects.order_by('name')

            for l in libraries:

                lib_order.append(l.name)
                
                plate_maps[l.__str__()] = self.getPlateMap(l, is_liquid)
        else:
        
            for nickname in nicknames:
                
#                 print("nickname: ", nickname)
            
                libraries = YeastLibrary_Model.objects.filter(personal_name=nickname).order_by('name')
    
                for l in libraries:
                    
                    plate_maps[l.__str__()] = self.getPlateMap(l, is_liquid)
    
            
#         print('plate_maps:', plate_maps)
        
        return [plate_maps, lib_order]
    
    
    
    def getPlateMap(self, lib, is_liquid):
        
        bare = {}
        
        bare['pk'] = lib.pk
        bare['name'] = lib.name
        
        bare_stacks = {}
        ordered_copy_keys = []
        
        for copy in YeastPlateStack_Model.objects.filter(library__pk = lib.pk, is_liquid = is_liquid).order_by('-time_stamp'):
            
            bare_stacks[copy.__str__()] = self.copyHelper.getMap(copy);
            ordered_copy_keys.append(copy.__str__())
            
            
        
        bare['stacks'] = bare_stacks   
        bare['ordered_copy_keys'] = ordered_copy_keys   
        
        return bare



class CopyHelper():
    """
    """
    
    def __init__(self):
        self.plateHelper = PlateHelper()
    
    
    def getBareDict(self, copy):
    
        bare = {}
        
        bare['name'] = copy.__str__()
        bare['pk'] = copy.pk
        
        
        
        bare_plates = []
        
        if copy.is_liquid:
            
            plates = LiquidYeastPlate_Model.objects.filter(yeast_plate__stack__pk = copy.pk).order_by('yeast_plate__scheme__index')
            
            for p in plates:
                
                map_ = p.yeast_plate.getMap()
                
                map_['plate_pk'] = map_['pk']
                map_['pk'] = p.pk
                
                bare_plates.append(map_)
            
        else:
            plates = YeastPlate_Model.objects.filter(stack__pk = copy.pk).order_by('scheme__index')
        
            for p in plates:
                
                bare_plates.append(self.plateHelper.getBareDict(p))
                
                
                
        
        bare['plates'] = bare_plates        
        
        return bare
    
    
    def getMap(self, copy):
    
        bare = {}
        
        bare['name'] = copy.__str__()
        bare['pk'] = copy.pk
        bare['time'] = copy.time_stamp.timestamp()
        
        bare_plates = []
        
        
        if copy.is_liquid:
            
            plates = LiquidYeastPlate_Model.objects.filter(yeast_plate__stack__pk = copy.pk).order_by('yeast_plate__scheme__index')
            
            for p in plates:
                
                map_ = p.yeast_plate.getMap()
                
                map_['plate_pk'] = map_['pk']
                map_['pk'] = p.pk
                
                bare_plates.append(map_)
            
        else:
            plates = YeastPlate_Model.objects.filter(stack__pk = copy.pk).order_by('scheme__index')
        
            for p in plates:
                
                bare_plates.append(p.getMap())
        
        
        bare['plates'] = bare_plates        
        
        return bare



   
class PlateHelper():
    """
    """    
    
    def __init__(self):
        self.snapshotBatchHelper = SnapshotBatchHelper()
    

    def getBareDict(self, plate):
    
        bare = {}
        
        bare['pk'] = plate.pk
        bare['index'] = plate.scheme.index
        
        bare_batches = []
        
        for b in SnapshotBatch_Model.objects.filter(plate__pk = plate.pk).order_by('index'):
            
            bare_batches.append(plate.snapshotBatchHelper.getBareDict(b))
        
        bare['batches'] = bare_batches        
        
        return bare
    
    
    
class SnapshotBatchHelper():

    def getBareDict(self, batch):
    
        bare = {}
        
        bare['pk'] = batch.pk
        bare['index'] = batch.index
        
        bare_snapshots = []
        
        for s in PlateSnapshot_Model.objects.filter(batch__pk = batch.pk):
            
            bare_snapshots.append(s.getBareDict())
        
        bare['snapshots'] = bare_snapshots        
        
        return bare
