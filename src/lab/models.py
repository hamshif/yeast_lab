from django.db import models


class ExperimentSchedule_Model(models.Model):
    """
    """
    
    schedule_csv = models.CharField(max_length=300, blank=True)
    fixed_interval = models.FloatField(default=0)
    duration = models.FloatField(default=0)
    onset_delay = models.FloatField(default=0)
    
    
class HardwareConfig_Model(models.Model):
    """
    An account of the hardware robot/comp configuration and properties 
    """
    application = models.CharField(max_length = 250, blank=True)
    device = models.CharField(max_length = 250, blank=True)
    firmware = models.CharField(max_length = 250, blank=True)
    user = models.CharField(max_length = 100, blank=True) # computer user id
    
    class Meta:
        unique_together = ('application', 'device', 'firmware', 'user')