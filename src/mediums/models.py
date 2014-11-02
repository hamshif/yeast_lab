from django.db import models

from suppliers.models import Source_Model
# Create your models here.

class ChemicalCompound_Model(models.Model):
    """ 
    This class represents an element or chemical compound.  
    """
    
    name = models.CharField(max_length = 50)
    chemical_description = models.TextField(max_length=250, blank=True)
    
    def __str__(self):
        return self.name



class Compound_Model(models.Model):
    """ 
    This class represents a compound in a mixture 
    e.g the kind, quantity and percentage of a substance in a hager medium.    
    """
    
    chemical = models.ForeignKey(ChemicalCompound_Model)
    quantity_in_miligrams = models.IntegerField()
    current_percentage = models.IntegerField(default=100)
    time_stamp = models.DateTimeField()
    source = models.ForeignKey(Source_Model, null=True, blank=True, default = None)
    
    def __str__(self):
        return self.name
    

class Batch_Model(models.Model):
    """ 
    This class represents an actual medium in an experiment plate
    """
    type = models.CharField(max_length = 50)
    time_stamp = models.DateTimeField()
    source = models.CharField(max_length=50)
    compounds = models.ManyToManyField(Compound_Model)
    
    
    def __str__(self):
        return self.type
    
    def asDict(self):
        ''        
        
        a = { 
              'type' : self.type,
              'primary_key': self.pk,
            }
        
        return a
    
    
    
    
    
#    maker = user