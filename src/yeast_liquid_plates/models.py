
from django.db import models

from yeast_libraries.models import YeastPlate_Model
from lab.models import ExperimentSchedule_Model, HardwareConfig_Model
from lab_util import calculate


        
class LiquidYeastPlate_Model(models.Model):
    
    yeast_plate = models.ForeignKey(YeastPlate_Model)
    plate_description = models.CharField(max_length = 100, blank=True)

    def __str__(self):
        return '_'.join(['liquid', self.yeast_plate.__str__()])   
    
        

class LiquidProcedure_Model(models.Model):
    
    experiment_schedule = models.ForeignKey(ExperimentSchedule_Model)
    target_od = models.FloatField(default=0)
    upper_bound_od = models.FloatField(default=0)
    measure_o_n = models.FloatField(default=0)
    dilution = models.FloatField(default=0)
    mca_tips_position = models.FloatField(default=0)
    
    well_volume = models.IntegerField(default=0)
    settle_time = models.FloatField(default=0)

    class Meta:
        unique_together = ('experiment_schedule', 'target_od', 'upper_bound_od', 'measure_o_n', 'dilution', 
                           'mca_tips_position', 'settle_time', 'well_volume')


class SpectrometerProcedure_Model(models.Model):
    """
    An account of the procedure the robot caries out
    
    0 in the fixed interval means that a comma separated schedule must be entered
    
    sampled indexes are a coma separated list of indexes of the type x;y corresponding to the marix width and height 
    """
    
    reades_per_well_border = models.IntegerField(default=1)
    wave_length = models.IntegerField(default=0)
    band_width = models.IntegerField(default=0)
    flashes = models.IntegerField(default=0)
    read_matrix_width = models.IntegerField(default=0)
    read_matrix_height = models.IntegerField(default=0)
    sampled_indexes_csv = models.CharField(max_length=200)
    
    target_temperature = models.FloatField(default=30)
    
    
    class Meta:
        unique_together = ('reades_per_well_border', 'wave_length', 'band_width', 'flashes', 
                           'read_matrix_width', 'read_matrix_height', 'sampled_indexes_csv', 'target_temperature')


class SpectrometerExperiment_Model(models.Model):
    """
    """
    
    plate = models.ForeignKey(LiquidYeastPlate_Model)
    hardware_config = models.ForeignKey(HardwareConfig_Model)
    liquid_procedure = models.ForeignKey(LiquidProcedure_Model)
    spectrometer_procedure = models.ForeignKey(SpectrometerProcedure_Model)
    description = models.CharField(max_length=300, blank=True)
    user = models.CharField(max_length = 50, blank=True)
    data_dir_name = models.CharField(max_length = 50, unique=True)
    
    dilution_time = models.DateTimeField()
    end_time = models.DateTimeField()
    
    
    def __str__(self):
        return '_'.join([self.data_dir_name, self.plate.__str__()])


class SpctrometerSample_Model(models.Model):
    """
    """
    experiment = models.ForeignKey(SpectrometerExperiment_Model)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    
    class Meta:
        unique_together = ('experiment', 'start_time', 'end_time')


class SpectrometerWellData_Model(models.Model):
    """
    the opacity_samples_csv field is a comma separated list of spectrometer readings from diffeent loci of the same well.
    The order of the readings corresponds to the sampled_indexes field in the corresponding SpectrometerProcedure_Model
    """
    
    sample = models.ForeignKey(SpctrometerSample_Model)
    row = models.IntegerField(default=1)    
    column = models.IntegerField(default=1)
    opacity_samples_csv = models.CharField(max_length=200)
    
    def getSamples(self):
        
        set_ = self.opacity_samples_csv.split(',')
        set_ = [float(i) for i in set_]
        
        return set_
    
    def getMean(self):
        
        return calculate.mean(self.getSamples())
    
    def getStdev(self):
    
        set_ = self.getSamples()
    
        return calculate.stdev(set_)



    class Meta:
        unique_together = ('sample', 'row', 'column')
    

    
    
class ParseDataProcess_Model(models.Model):
    """
    An indicator of the state of the a process of parsing experiment data from directory and persisting it to the DB  
    """
    
    dir_path = models.CharField(max_length=300)
    status = models.CharField(max_length=40, blank=True)
    experiment = models.ForeignKey(SpectrometerExperiment_Model, blank=True, null=True, default=None)
    
    def __str__(self):    
        
        return ' '.join(['status:', self.status])

    
        
