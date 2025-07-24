
import numpy as np
import ROOT

# TODO add class for statistic results
class data_generator:
    def __init__(self,xmin,xmax,Npoints):
        self.xmin       =xmin
        self.xmax       =xmax
        self.Npoints    =Npoints
        
        self.x = np.linspace(xmin, xmax, Npoints)
        self.y=None

    def set_waveform_func(self,func):
        self.y = func(self.x)
    def get_waveform(self):
        return self.x, self.y
