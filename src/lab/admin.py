from django.contrib import admin

from lab.models import ExperimentSchedule_Model, HardwareConfig_Model

from yeast_libraries.models import PlateFormat_Model, YeastStrain_Model, PlateLocus_Model, PlateScheme_Model\
,YeastLibrary_Model, YeastPlate_Model, PlateSnapshot_Model, YeastPlateStack_Model\
, StorageLocation_Model, LocusAnalysis_Model, SnapshotBatch_Model, SnapshotProcess_Model
from mediums.models import ChemicalCompound_Model, Compound_Model,Batch_Model
from suppliers.models import Source_Model
from yeast_liquid_plates.models import SpectrometerProcedure_Model, SpectrometerWellData_Model\
,SpctrometerSample_Model, SpectrometerExperiment_Model, LiquidProcedure_Model, LiquidYeastPlate_Model 


admin.site.register(Source_Model)

admin.site.register(ExperimentSchedule_Model)
admin.site.register(HardwareConfig_Model)


admin.site.register(ChemicalCompound_Model)
admin.site.register(Compound_Model)
admin.site.register(Batch_Model)

admin.site.register(StorageLocation_Model)
admin.site.register(PlateFormat_Model)
admin.site.register(YeastStrain_Model) 
admin.site.register(PlateLocus_Model)
admin.site.register(PlateScheme_Model)
admin.site.register(YeastLibrary_Model)
admin.site.register(YeastPlate_Model) 
admin.site.register(PlateSnapshot_Model)
admin.site.register(YeastPlateStack_Model)
admin.site.register(LocusAnalysis_Model)
admin.site.register(SnapshotBatch_Model)
admin.site.register(SnapshotProcess_Model)

admin.site.register(LiquidYeastPlate_Model)
admin.site.register(LiquidProcedure_Model)
admin.site.register(SpectrometerProcedure_Model)
admin.site.register(SpectrometerWellData_Model)
admin.site.register(SpctrometerSample_Model)
admin.site.register(SpectrometerExperiment_Model)

