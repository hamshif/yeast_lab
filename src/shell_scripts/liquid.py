

from yeast_liquid_plates.models import SpectrometerExperiment_Model,\
    ParseDataProcess_Model, SpectrometerWellData_Model, LiquidYeastPlate_Model



print('kanookee')

def a():

    samples = SpectrometerWellData_Model.objects.filter()

    for sample in samples:

        print('str(sample.getStdev()):  ', str(sample.getStdev()))



def b():

    print('cloak')

    experiments = SpectrometerExperiment_Model.objects.filter()

    for experiment in experiments:

        print('experiment:  ', experiment.__str__())



print('cloaker')

experiments = SpectrometerExperiment_Model.objects.all()

for experiment in experiments:

    print('experiment:  ', experiment.__str__())