import ROOT
import math
class fuc_SiPM_IV_3rd_der:
    def __call__(self, vars, pars):
        '''
        This function is a model used to describe the 3rd derivative of SiPM IV curve
        from paper: https://doi.org/10.1016/j.nima.2017.01.002
        vars:
            0 ==> V
        pars:
            0 ==> A: amplitude
            1 ==> sigma: std dev
            2 ==> V01: breakdown voltage
            3 ==> h: hysteresis
        '''
        V = vars[0]
        A = pars[0]
        sigma = pars[1]
        V01 = pars[2]
        h = pars[3]
        I = A*(2-h*(V-V01)/sigma**2)*math.exp(-(V-V01)**2/(2*sigma**2))
        return I