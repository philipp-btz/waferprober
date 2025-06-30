from ftplib import parse150
import numpy as np
import math 
import ROOT

class IV_analysiser:
    k_b = 8.617333e-5       #boltzman constant
    C_to_K_Const=273.15     
    E_a=0
    def __init__(self):
        pass
    def set_Ea(self,E_a):
        self.E_a = E_a

    def current_corr(self,gr,R=1000.):## this is the function to correct the voltage drop on the current limit R, default 1 kohm
        gr_tmp=ROOT.TGraph()
        for i in range(gr.GetN()):
            gr_tmp.SetPoint(i,gr.GetX()[i]-gr.GetY()[i]*R,gr.GetY()[i])
        return gr_tmp
    
    def gr_ZeroCorr(self,gr,x_ref=0):    ## to correct everything to given x_ref
        n= gr.GetN()
        x = np.asarray(gr.GetX())
        y = np.asarray(gr.GetY())-gr.Eval(x_ref)
        return ROOT.TGraph(n,x,y)

    def get_Vbr_relDiv(self,gr):
        n= gr.GetN()
        x = np.asarray(gr.GetX())
        x_shift = x+(x[1]-x[0])/2.  # shift it with half gap of x_gap
        y_log = np.log10(np.asarray(gr.GetY())-np.min(np.asarray(gr.GetY()))+1e-9) #get log10
        y_diff = np.diff(y_log)/np.diff(x)
        return int(np.where(y_diff==np.amax(y_diff))[0]), ROOT.TGraph(n-1,x_shift,y_diff), ROOT.TGraph(n,x,y_log) 

    def get_Max_inRange(self,gr,x_low,x_high,en_Spline=False,Spline_step=0.01): 
        n= gr.GetN()
        x = np.asarray(gr.GetX())
        y = np.asarray(gr.GetY())
        y_max=gr.Eval(x_low)
        x_max=x_low
        if en_Spline:
            gr_sp = ROOT.TGraph()
            sp=ROOT.TSpline5("spline_runID",gr)
            for x_curr in np.arange(x_low,x_high,Spline_step):
                y_curr = sp.Eval(x_curr)
                gr_sp.SetPoint(gr_sp.GetN(),x_curr,y_curr)
                if y_curr >y_max:
                    y_max = y_curr
                    x_max = x_curr
            return x_max, gr_sp
        else:
            for i in range(n):
                if x<x_low or x>x_high:
                    continue
                if y[i]>y_max:
                    y_max=y[i]
                    x_max=x[i]
            return x_max,y_max
    

    def get_OV(self,gr,Vbr,en_Spline=False): #plot the IV curve with X is Overvoltage(OV)
        n= gr.GetN()
        x = np.asarray(gr.GetX())-Vbr
        y = np.asarray(gr.GetY())
        if(en_Spline):
            return ROOT.TGraph(n,x,y)
        else:
            return ROOT.TGraph(n,x,y)
        
    def createIVwithErrors(self,gr):
        n= gr.GetN()
        x = np.asarray(gr.GetX())
        y = np.asarray(gr.GetY())
        y_err=y*0.02+200e-9
        gr_tmp=ROOT.TGraphErrors(n,x,y,0,y_err)
        return gr_tmp

    def get_I_ConstOV(self,grs,OV):
        y=[]
        for gr in grs:
            if OV < np.asarray(gr.GetX())[-1]:
                y.append(gr.Eval(OV))
        return y
    def constant_fit(self,gr,x_low=39.6, x_high=45.,par_name="Constant"):
        '''most normal linear fit'''
        f_fit = ROOT.TF1("f_fit","[0]",x_low,x_high)
        f_fit.SetParNames(par_name)
        gr.Fit(f_fit,"RQ")
        gr.Fit(f_fit,"RQ")
        return np.asarray(f_fit.GetParameters()),np.asarray(f_fit.GetParErrors()),f_fit.GetChisquare()/f_fit.GetNDF()
    def lin_fit(self,gr,x_low=39.6, x_high=45.,par_name1="dV/dT",par_name2="V_{f0}"):
        '''most normal linear fit'''
        f_fit = ROOT.TF1("f_fit","[0]*x+[1]",x_low,x_high)
        f_fit.SetParNames(par_name1,par_name2)
        gr.Fit(f_fit,"RQ")
        gr.Fit(f_fit,"RQ")
        return np.asarray(f_fit.GetParameters()),np.asarray(f_fit.GetParErrors()),f_fit.GetChisquare()/f_fit.GetNDF()
    def lin_fit1(self,gr,x_low=39.6, x_high=45.,par_name1="E_{a}",par_name2="Constant"):
        f_fit = ROOT.TF1("f_fit","-[0]*x+[1]",x_low,x_high)
        f_fit.SetParNames(par_name1,par_name2)
        x = np.asarray(gr.GetX())
        y = np.asarray(gr.GetY())
        slope = (np.max(y)-np.min(y))/(np.max(x)-np.min(x))
        y_offset = gr.Eval((x_low+x_high)/2.)+slope*(x_low+x_high)/2.
        f_fit.SetParameters(slope,y_offset)
        f_fit.SetParLimits(0,slope-0.1,slope+0.1)
        f_fit.SetParLimits(1,y_offset-1.,y_offset+1.)
        print(f"pars set: {slope},{y_offset}")
        gr.Fit(f_fit,"RQ")
        return np.asarray(f_fit.GetParameters()),np.asarray(f_fit.GetParErrors()),f_fit.GetChisquare()/f_fit.GetNDF()

    def lin_fit2(self,gr,x_low=-3., x_high=-0.5,par_name0="R",par_name1="V_{f}"):
        '''this is used for forward I-V curve fitting'''
        f_fit = ROOT.TF1("f_fit","-(x+[1])/[0]",x_low,x_high) #the v is negetive
        f_fit.SetParNames(par_name0,par_name1)
        y_high = gr.Eval(x_high)
        y_low  = gr.Eval(x_low)
        par0   = -(x_high-x_low)/(y_high-y_low)
        par1   = -(x_high+y_high*par0)
        f_fit.SetParameters(par0,par1)
        #f_fit.SetParLimits(0,slope-0.1,slope+0.1)
        #f_fit.SetParLimits(1,y_offset-1.,y_offset+1.)
        print(f"pars set: {par0},{par1}")
        gr.Fit(f_fit,"RQ")
        gr.Fit(f_fit,"RQ")
        return np.asarray(f_fit.GetParameters()),np.asarray(f_fit.GetParErrors()),f_fit.GetChisquare()/f_fit.GetNDF()

    def exp_fit(self,gr,x_low, x_high):
        f_fit = ROOT.TF1("f_fit","[0]*exp(-x/[1])+[2]",x_low,x_high)
        f_fit.SetParNames("#DeltaI","#tau","I_{rest}")
        I0=gr.GetY()[0]
        I_rest = gr.GetY()[gr.GetN()-1]
        f_fit.SetParameters(I0-I_rest,5.,I_rest)
        #f_fit.SetParLimits(0,0.,2*gr.GetY()[0])
        f_fit.SetParLimits(1,0.,60.)
        gr.Fit(f_fit,"RQ")
        pars = np.asarray(f_fit.GetParameters())
        f_fit.SetParameters(pars[0],pars[1],pars[2])
        status = gr.Fit(f_fit,"RQ")
        if int(status) !=0:
            gr.Fit(f_fit,"RQ")
        return np.asarray(f_fit.GetParameters()),np.asarray(f_fit.GetParErrors()),f_fit.GetChisquare()/f_fit.GetNDF()

    def fit_I_vs_T(self,gr,x_low, x_high, rescale=False, T_norm=10):
        f_fit = ROOT.TF1("f_fit","[0]*exp(x/[1])",x_low,x_high)
        f_fit.SetParNames("Constant","T_{0}")
        #I0=gr.GetY()[0] 
        f_fit.SetParameters(gr.Eval(0),15.)
        #f_fit.SetParLimits(0,0.,1.)
        gr.Fit(f_fit,"RQ")
        gr.Fit(f_fit,"RQ")
        if rescale:
            print(f"Rescale the graph with the T_norm: {T_norm} degree")
            self.scale_gr(gr,1./f_fit.Eval(T_norm))
        gr.Fit(f_fit,"RQ")
        return np.asarray(f_fit.GetParameters()),np.asarray(f_fit.GetParErrors()),f_fit.GetChisquare()/f_fit.GetNDF()
    
    def scale_gr(self,gr, scale):
        '''
        y = y*scale
        '''
        for i_pt in range(int(gr.GetN())):
            gr.SetPoint(i_pt,gr.GetX()[i_pt],gr.GetY()[i_pt]*scale)
            gr.SetPointError(i_pt,gr.GetEX()[i_pt],gr.GetEY()[i_pt]*scale)
    def double_exp_fit(self,gr,x_low, x_high):
        f_fit = ROOT.TF1("f_fit","[0]*exp(-x/[1])+[2]*exp(-x/[3])+[4]",x_low,x_high)
        f_fit.SetParNames("#DeltaI_{fast}","#tau_{fast}","#DeltaI_{slow}","#tau_{slow}","I_{rest}")
        I0=gr.GetY()[0] 
        f_fit.SetParameters(I0/2.,0.5,I0/2.,4,0.5*I0)
        f_fit.SetParLimits(0,0.,I0)
        f_fit.SetParLimits(1,0.,2.)
        f_fit.SetParLimits(2,0.,I0)
        f_fit.SetParLimits(3,3.,15.)
        f_fit.SetParLimits(4,0.,I0)
        gr.Fit(f_fit,"RQ")
        f_fit.SetParameters(np.asarray(f_fit.GetParameters()))
        gr.Fit(f_fit,"RQ")
        return np.asarray(f_fit.GetParameters()),np.asarray(f_fit.GetParErrors()),f_fit.GetChisquare()/f_fit.GetNDF()
    def get_Icorr_based_on_T(self,gr_T,T_ref):  # gr_T should be T at different Run
        T_ref=T_ref+self.C_to_K_Const    #change to Kelvin degree
        n= gr_T.GetN()
        x = np.asarray(gr_T.GetX()) #runID
        y = np.asarray(gr_T.GetY())+self.C_to_K_Const 
        zz=self.E_a/self.k_b*(1./T_ref-1./y)
        print(zz) 
        factor = math.e**(zz) #I/I_0: Ea/k*(1/T_0-1/T)
        #factor = math.e**(self.E_a/self.k_b*(1./T_ref-1./y)) #I/I_0: Ea/k*(1/T_0-1/T)
        return ROOT.TGraph(n,x,factor)
    def get_Icorr_based_on_T_exp(self,gr_T,T_ref):
        '''
            I = A*exp(T/T_0)
            where T_0 should be the 15.7 measured from the T dependence part
        '''
        T_0 = 15.7
        n= gr_T.GetN()
        x = np.asarray(gr_T.GetX()) #runID
        y = np.asarray(gr_T.GetY())
        factor = math.e**((y-T_ref)/T_0)
        return ROOT.TGraph(n,x,factor)

    def get_Icorr_based_on_Vbr(self,gr_Vbr,Vbr_ref,T_ref,T_Vbr_coeff):  # gr_Vbr should be Vbr at different Run; 
        T_ref=T_ref+self.C_to_K_Const    #change to Kelvin degree
        n= gr_Vbr.GetN()
        x = np.asarray(gr_Vbr.GetX()) #runID
        y = np.asarray(gr_Vbr.GetY()) 
        factor = math.e**(self.E_a/self.k_b*((y-Vbr_ref)/T_Vbr_coeff/T_ref/T_ref)) #I/I_0 : 
        return ROOT.TGraph(n,x,factor)
    def get_Icorr_based_on_Vbr_exp(self,gr_Vbr,Vbr_ref,T_Vbr_coeff):  # gr_Vbr should be Vbr at different Run; 
        '''
            This method will only work well when the OV is 
            I = A*exp(T/T_0) ==> factor =  exp((T-T_ref)/T_0)
            where T_0 should be the 15.7 measured from the T dependence part
            T-T_ref = (Vbr-Vbr_ref)/T_Vbr_coeff  ==> factor = exp((Vbr-Vbr_ref)/T_0/TVbr_coeff)
        '''
        T_0 = 15.7
        n= gr_Vbr.GetN()
        x = np.asarray(gr_Vbr.GetX()) #runID
        y = np.asarray(gr_Vbr.GetY())
        factor = math.e**((y-Vbr_ref)/T_Vbr_coeff/T_0)
        return ROOT.TGraph(n,x,factor)
    def Ierror_from_Terror(self,I,T,Terror):
        T = T+self.C_to_K_Const
        return I*(self.E_a/self.k_b/T)*(Terror/T)
    def mapping_ch_to_dose(self,gr_measure,gr_dose,gr_mapping,bool_measure_with_error=True):
        '''
        gr_mapping: 
            x ==> ch in measurement
            y ==> ch in simulation
        '''
        n_meas = gr_measure.GetN()
        x_meas = np.asarray(gr_measure.GetX())
        y_meas = np.asarray(gr_measure.GetY())
        ex_meas = 0
        ey_meas = 0
        if bool_measure_with_error:
            ex_meas = np.asarray(gr_measure.GetEX())
            ey_meas = np.asarray(gr_measure.GetEY())

        n_dose = gr_dose.GetN()
        x_dose = np.asarray(gr_dose.GetX())
        y_dose = np.asarray(gr_dose.GetY())

        gr_rnt = ROOT.TGraph()
        if bool_measure_with_error:
            gr_rnt = ROOT.TGraphErrors()

        for i in range(n_meas):
            ch_dose = gr_mapping.Eval(x_meas[i])
            dose_index =-1
            for j in range(n_dose):
                if abs(x_dose[j]-ch_dose)<0.1:
                    dose_index = j
                    break
            if dose_index ==-1:
                dose_curr = 0.
            else:
                dose_curr = y_dose[dose_index]
            gr_rnt.SetPoint(gr_rnt.GetN(),dose_curr,y_meas[i])
            if bool_measure_with_error:
                gr_rnt.SetPointError(gr_rnt.GetN()-1,0.,ey_meas[i])
        return gr_rnt
