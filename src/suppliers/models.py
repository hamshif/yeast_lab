'''
Created on Feb 3, 2014

@author: gideonbar
'''
from django.db import models

class Source_Model(models.Model):
    """ 
    This class represents a compound in a mixture 
    e.g the kind, quantity and percentage of a substance in a hager medium.    
    """
    
    name = models.CharField(max_length = 50)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length = 10, blank=True)
    description = models.TextField(max_length=250)

    def __str__(self):
        return self.name