
import sys, traceback
from django.db import models
from mediums.models import Batch_Model
from django.template.defaultfilters import default
import yeast_libraries
from lab_util import util  






class StorageLocation_Model(models.Model):
    """
    """
    location = models.CharField(max_length=50, unique=True)
    conditions = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.location



class YeastLibrary_Model(models.Model):
    """ 
    This class holds plate schemes for a set of strains usually with a common denominator e.g common ancestor.
    """
    name = models.CharField(max_length=50, unique=True)
    link = models.URLField(blank=True)
    personal_name = models.CharField(max_length=50, default='everyone')
    
    
    def __str__(self):
        return self.name
    
    
    def asDict(self):
        bare = {}
        
        bare['pk'] = self.pk
        bare['name'] = self.name
    
        return bare



class PlateFormat_Model(models.Model):
    """
    A matrix describing the compartmentalization of a rectangular plastic dish into compartments of same size
    """
    width = models.IntegerField(default=0, blank=True)
    length = models.IntegerField(default=0, blank=True)
    width_loci = models.IntegerField(default=0)
    length_loci = models.IntegerField(default=0)
    
    def __str__(self):
        return '_'.join(['-'.join([str(self.length_loci), str(self.width_loci)]), 'Plate'])
    


class PlateScheme_Model(models.Model):
    """
    This class map's formats to a plate index in yeast library
    """
    format = models.ForeignKey(PlateFormat_Model)
    library = models.ForeignKey(YeastLibrary_Model)
    index = models.IntegerField(default=1)
    
    def __str__(self):
        
        s = ' '.join(['plate:', str(self.index), 'in library:', self.library.__str__()])
        
        return s

    class Meta:
        
        unique_together = (("format", "library", "index"),) #will include users


    
class YeastStrain_Model(models.Model):
    """ 
    This class represents a Yeast Strain defined by its genotype, sometimes Gene/ORF Name.
    the parents column is many to many only because there could be more than one prarent strain
    """
    
    name = models.CharField(max_length=50, unique=True)
    parents = models.ManyToManyField('self', blank=True)
    system_name = models.CharField(max_length=50, blank=True)
    link = models.URLField(blank=True)
    
    def __str__(self):
        return self.name
    
    
    
    
class YeastPlateStack_Model(models.Model):
    """
    The physical manifestation of a stack of plates with colonies of yeast strains
    """
    library = models.ForeignKey(YeastLibrary_Model) 
    parent = models.ForeignKey('self', blank=True, null=True, default=None, on_delete=models.SET_NULL)
    is_liquid = models.BooleanField(default=False)
    time_stamp = models.DateTimeField()
    medium = models.ForeignKey(Batch_Model, blank=True, null=True, on_delete=models.SET_NULL)
    
    storage = models.ForeignKey(StorageLocation_Model, blank=True, null=True, on_delete=models.SET_NULL)
    
#     user = models.CharField(max_length = 50, blank=True) #TODO add user and make this field compulsory
    
    def __str__(self):
        
        d = self.time_stamp        
        
        dt = self.time_stamp.date().__str__() + '-' + d.time().__str__()[0:5]
        
        s = 'agar'
        
        if self.is_liquid:
            s = 'liquid'
        
        
        return '_'.join([self.library.__str__(), s, dt])

    
    def asDict(self):
        bare = {}
        
        bare['pk'] = self.pk
        bare['name'] = self.__str__()
        
        bare['time'] = self.time_stamp.timestamp()
        
        if self.parent == None:
            bare['parent'] = self.parent
        else:
            bare['parent'] = self.parent.pk
    
        return bare
    
    
     
    class Meta:
        unique_together = (("library", "time_stamp"),) #will include users



class YeastPlate_Model(models.Model):
    """
    The physical manifestation of a plate of yeast colonies
    """
    
    scheme = models.ForeignKey(PlateScheme_Model)
    stack = models.ForeignKey(YeastPlateStack_Model)
    time_stamp = models.DateTimeField(blank=True)
    conditions = models.CharField(max_length = 50, blank=True)
    user = models.CharField(max_length = 50, blank=True) 
    
    def __str__(self):
        return ' '.join(['plate', str(self.scheme.index)])
    
    
    def full_str(self):
        ''
        return ' '.join(['copy: ', self.stack.__str__(), '     plate: ', str(self.scheme.index)])
    
    
    def getDataShellDict(self):

        d = {}
        
        d['library_pk'] = self.stack.library.pk
        d['stack_pk'] = self.stack.pk
        d['pk'] = self.pk
        d['index'] = self.scheme.index
        d['name'] = self.__str__()
    
        return d
    
    
    def getMap(self):
    
        bare = {}
        
        bare['pk'] = self.pk
        bare['index'] = self.scheme.index      
        
        return bare
    
    

    class Meta:
        
        unique_together = (("scheme", "stack"),) #will include users





class PlateLocus_Model(models.Model):
    """
    This class allocates a strain to a specific compartment in a plate
    """
    scheme = models.ForeignKey(PlateScheme_Model)
    strain = models.ForeignKey(YeastStrain_Model, null=True, default=None)
    column = models.IntegerField(default=0)
    row = models.CharField(max_length=4)
    
    def __str__(self):
        return ' '.join([self.strain.__str__(), 'plate:', str(self.scheme.index), 'column:', str(self.column), 'row:', self.row])
    
    def rowAsNum(self):
        
        return util.stringNumericalValue(self.row)





class SnapshotBatch_Model(models.Model):
    """
    A batch of snapshots usualy for time conditions 
    necessary for time lapse feature
    """ 
    
    plate = models.ForeignKey(YeastPlate_Model)
    index = models.IntegerField(default=1)
#     snapshots = models.ManyToManyField(PlateSnapshot_Model, blank=True, null=True, default = None)
    
    def __str__(self):
        return ' '.join(['batch', str(self.index), 'of', self.plate.__str__()])
    
    
    


class PlateSnapshot_Model(models.Model):
    """
    A snapshot of a plate at certain time and conditions 
    """
    
    batch = models.ForeignKey(SnapshotBatch_Model)
    image_path = models.CharField(max_length=250)
    processed_image_path = models.CharField(max_length=250, blank=True)
    time_stamp = models.DateTimeField(null=True, blank=True)
    conditions = models.CharField(max_length = 50, blank=True)
    user = models.CharField(max_length = 50, blank=True) #TODO add user and make this field compulsory
#     analysis = models.ManyToManyField(LocusAnalysis_Model, blank=True, null=True, default=None)
    
    def __str__(self):
        return ' '.join([self.batch.plate.stack.__str__(), self.batch.plate.__str__()])

    
    def getBareDict(self):
        
        bare = {}
        
        bare['pk'] = self.pk
        bare['image_path'] = self.image_path
        bare['processed_image_path'] = self.processed_image_path
        
        
        return bare
    
    
    class Meta:
        
        unique_together = (("batch", "image_path"),) #will include users



class LocusAnalysis_Model(models.Model):
    """
    """
    
    snapshot = models.ForeignKey(PlateSnapshot_Model)
    locus = models.ForeignKey(PlateLocus_Model, blank=True, null=True, on_delete=models.SET_NULL)
    is_empty = models.BooleanField(default = True)
    area_scaled = models.IntegerField(default = 1)
    column = models.IntegerField(default = 1)
    row = models.IntegerField(default = 1)
    ratio = models.IntegerField(default = 1)
    center_x = models.IntegerField(default = 1)
    center_y = models.IntegerField(default = 1)

    def __str__(self):
        
        if self.is_empty == True:
            
            return ' '.join(['colony', 'r:', str(self.row), 'c:',  str(self.column),  'is empty'])
            
        else:
            return ' '.join(['colony', 'r:', str(self.row), 'c:',  str(self.column),  'exists'])
        
        
    def getAsList(self):
        
        as_list = []
        as_list.append(self.column)
        as_list.append(self.row)
        as_list.append(self.is_empty)
        as_list.append(self.area_scaled)
        as_list.append(self.ratio)
        as_list.append(self.center_x)
        as_list.append(self.center_y)
        
        return as_list 


    
class SnapshotProcess_Model(models.Model):
    """
    The physical manifestation of a stack of plates with colonies of yeast strains
    """
    snapshot_pk = models.IntegerField(unique=True)
    status = models.CharField(max_length=40, blank=True)
    
    def __str__(self):
    
        d = self.snapshot_pk        
        
        
        return ' '.join(['snapshot_pk:', str(d), 'status:', self.status])
    


