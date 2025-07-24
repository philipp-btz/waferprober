#Tiancheng Zhong 2021.07
from re import I
import spectrum as spc ##FIXME: attention the methods used in this file to calculate psd is wrong!!!! need to fix
import numpy as np
from scipy.fft import fft, fftfreq
from scipy import signal
import ROOT
from cppyy import nullptr

from my_python_package.plot_helper.plot_helper import plot_helper 
plot_hp = plot_helper()

class noise_ana:
    class sig_filter:
        _filter_sos =[]
        _filter_b   =[]
        _filter_a   =[]
        sr_resample = 0
        y_resample = []
        Wn =None      # low pass edge in Hz
        order =8    # filter order
        btype='lowpass' #pass type
        analog=False    #True: analog filter; False: digital filter
        output='sos'    #output type of filter
        def set_filter(self,sr_resample, Wn):
            self.sr_resample = sr_resample
            self.Wn = Wn
        def set_order(self,order):
            self.order = order
        def get_y_resample(self,N=-1):
            if N<0:
                return self.y_resample
            else:
                return self.y_resample[:N]
        def get_sr_resample(self):
            return self.sr_resample
        def reset_y_resample(self):
            self.y_resample=[]

    def __init__(self,hv,ch,sr,gr):
        self.channel = ch   #ID for this SiPM
        self.hv = hv        #hv on SiPM with unit of V
        self.sr = sr        #sampling rate with unit of Hz
        self.gr = gr        #data with form of ROOT.TGraph
        self.win = None
        self.y = np.asarray(gr.GetY())
        self.y_filtered = []
        self.y_win = np.asarray(gr.GetY())
        self.N = len(self.y)
        self.xf=[]
        self.yf=[]
        self.period = (gr.GetX()[self.N-1]-gr.GetX()[0]+gr.GetX()[1]-gr.GetX()[0])*1.e-9
        self.filter = self.sig_filter()
        #self.print_inf()
    def print_inf(self):
        print("hv: ",self.hv)
        print("ch: ",self.channel)
        print("N points in graph: ",self.gr.GetN())
    
    def gen_filter(self):
        self.filter._filter_sos = signal.butter(N=self.filter.order,Wn=self.filter.Wn,btype=self.filter.btype,analog=self.filter.analog,output=self.filter.output,fs=self.sr)
        print("gen_filter() done!")
    def get_hv(self):
        return self.hv
    
    def get_channel(self):
        return self.channel

    def get_psd_FT_corr(self,lag=20): #Fourier method based upon correlogram
        sp = spc.pcorrelogram(np.asarray(self.gr.GetY()),lag=lag, sampling=self.sr,scale_by_freq=True)
        return sp
    def get_psd_FT_period(self):
        sp = spc.Periodogram(np.asarray(self.gr.GetY()), sampling=self.sr, scale_by_freq=False, window="hanning" )
        return self._psd_to_TGraph(sp)

    def get_psd_ARMA(self,P,Q,lag,mean_zero=True): #P:Desired number of AR parameters;  P:Desired number of MA parameters; lag=Maximum lag to use for autocorrelation estimates
        data = self.y
        if mean_zero:
            data = data - np.mean(self.y)
        sp = spc.parma(data, P,Q,lag,self.N, sampling=self.sr,scale_by_freq=True)
        return self._psd_to_TGraph(sp,self.period)
    
    def do_criteria_ARMA(self,p_max,lag,name_crit="AIC"):
        min_data =None
        min_id =(0,0)
        A_min = None
        B_min = None
        h2 = ROOT.TH2D("criteria_arma","Parameter criteria for ARMA estimation; AR order P; MA parameter Q; AIC value",p_max,0.5,p_max+0.5,p_max,0.5,p_max+0.5)
        for k in range(1,p_max,1): # AR order
            for j in range(1,k,1): # MA number
                A,B,rho = spc.arma.arma_estimate(self.y,k,j,lag)
                data = spc.criteria.AIC(self.N,rho,k)/self.N
                h2.Fill(k,j,data)
                print(f"do_estimate [{k},{j}]: {data}")
                if min_data==None or min_data>data:
                    min_data = data
                    min_id = (k,j)
                    A_min = A
                    B_min = B
                    rho_min = rho
        print(f"Best:lag={lag},[p,q]= [{min_id}]: {min_data}")
        return min_id,h2,min_data,A_min,B_min,rho_min
    def _psd_to_TGraph(self,sp,norm=1.):
        gr=ROOT.TGraph(len(sp.psd),np.asarray(sp.frequencies()),sp.psd/norm)
        return gr
    def set_window(self, win):
        self.win = win
    def set_graph(self, gr):
        self.gr = gr        #data with form of ROOT.TGraph
        self.y = np.asarray(gr.GetY())
        self.y_win = np.asarray(gr.GetY()) 
        self.N = len(self.y)
    def set_sr(self,sr):
        self.sr=sr
    
    def cal_fft_amp(self):
        print("get_fft()...")
        norm_win = 1.
        if self.win!=None:
            window = self.win(self.N)
            self.y_win= self.y*window
            norm_win = np.sum(self.win(self.N))/self.N

        self.xf = fftfreq(self.N, 1./self.sr)[:self.N//2]
        self.yf = norm_win*np.abs(fft(self.y_win)) 
        self.yf[0] = self.yf[0]/2. # the constant one should not be times 2 
        #return xf,yf
    def get_fft_spec(self):
        if len(self.yf)==0:
            self.cal_fft_amp()
        gr=ROOT.TGraph(len(self.xf),self.xf,self.yf*2./self.N)    
        return gr
    def get_psd(self):
        if len(self.yf)==0:
            self.cal_fft_amp()
        f_res = self.sr/self.N
        psd_norm = self.yf**2.*2./self.N**2./f_res
        psd_norm[0]*=2. #power of DC do not need to divided by 2
        gr=ROOT.TGraph(len(self.xf),self.xf,psd_norm)
        return gr
    def get_psd_logx(self):
        if len(self.yf)==0:
            self.cal_fft_amp()
        f_res = self.sr/self.N
        psd_norm = self.yf**2.*2./self.N**2./f_res
        psd_norm[0]*=2. #power of DC do not need to divided by 2
        N_point = len(self.xf)
        gr=ROOT.TGraph(N_point-2,np.log10(self.xf[1:N_point-1]),psd_norm[1:N_point-1])
        return gr
    def average_graph(self, gr_in,IsLogX=True,bin_gap=0.01):
        x = np.asarray(gr_in.GetX())
        y = np.asarray(gr_in.GetY())
        N_index = len(x)
        gr_out=ROOT.TGraphErrors()
        index_start=0
        x_start = x[0]
        print(IsLogX,bin_gap)
        for index in range(1,N_index):
            if (IsLogX and (x[index]>(x_start+bin_gap))) or (not IsLogX and x[index]>x_start*10**bin_gap) or index == N_index-1:
                if index-1 == index_start:
                    gr_out.SetPoint(gr_out.GetN(),x[index_start],y[index_start])
                else:
                    gr_out.SetPoint(gr_out.GetN(),np.mean(x[index_start:index-1]),np.mean(y[index_start:index-1]))
                    gr_out.SetPointError(gr_out.GetN()-1,np.std(x[index_start:index-1]),np.std(y[index_start:index-1]))
                #gr_out.SetPoint(gr_out.GetN(),np.mean(x[index_start:index-1]),np.mean(y[index_start:index-1]))
                index_start = index
                x_start = x[index]
        return gr_out
    def get_ps(self):
        if len(self.yf)==0:
            self.cal_fft_amp()
        psd = self.yf**2.*2./self.N**2.
        psd[0]*=2.  #power of DC do not need to divided by 2
        gr=ROOT.TGraph(len(self.xf),self.xf,psd)
        return gr
    def get_psd_welch(self,N_seg,resample=False,filtered=False,average='mean'):
        x=None
        y=None
        if resample == True:
            x,y=signal.welch(x=self.filter.y_resample,fs=self.filter.sr_resample,nperseg=len(self.filter.y_resample)//N_seg,nfft=len(self.filter.y_resample),average=average)
        elif filtered==True:
            x,y=signal.welch(x=self.y_filtered,fs=self.sr,nperseg=self.N//N_seg,nfft=self.N,average=average)
        else:
            x,y=signal.welch(x=self.y,fs=self.sr,nperseg=self.N//N_seg,nfft=self.N,average=average)

        gr=ROOT.TGraph(len(x),x,y)
        return gr
    def tgraph_to_csv(self,gr,csv_name,Nignore_pre=0):
        x = np.asarray(gr.GetX())
        y = np.asarray(gr.GetY())
        file_csv = open(csv_name,"w")
        #for iPoint in range(10000):
        for iPoint in range(gr.GetN()):
            #file_csv.write(f"{x[iPoint]:}")
            #file_csv.write(",")
            file_csv.write(f"{y[iPoint]:.1f},")
            #file_csv.write("\n")
            if iPoint>Nignore_pre:
                continue
        file_csv.close()
    
    def do_filt_signal(self,filter_type=1):
        print("do_filter...")
        if len(self.filter._filter_sos) ==0:
            print("filter is not defined yet. please call function gen_filter()")
            return -1
        else:
            print(f"N of numbers before filter: {len(self.y)}")
            if filter_type ==1:
                self.y_filtered = signal.sosfilt(self.filter._filter_sos,self.y-np.mean(self.y)) + np.mean(self.y)
            if filter_type ==2:
                self.y_filtered = signal.sosfiltfilt(self.filter._filter_sos,self.y-np.mean(self.y)) + np.mean(self.y)
            print(f"N of numbers after filter: {len(self.y_filtered)}")
    def get_signal(self,n_shown=10000,filtered=True,resampled=False):
        if(n_shown>len(self.y_filtered)):
            n_shown = len(self.y_filtered)
        if filtered==True:
            if resampled==False:
                return self.y_filtered[:n_shown]
            else:
                return self.filter.y_filtered[:n_shown*self.sr//self.filter.sr_resample]
        else:
            return self.y[:n_shown-1]
    def do_resampling(self):
        print("do_resampling..")
        if len(self.y_filtered) ==0:
            print("do_resampling()::filtered waveform is empty")
            return -1
        if self.sr%self.filter.sr_resample !=0:
            print(f"{self.sr}/{self.filter.sr_resample} is not a integer. for this case, it's not implemented")# TODO
            return -1
        N_gap = self.sr//self.filter.sr_resample
        print(f"sr,sr_resample,gap: {self.sr},{self.filter.sr_resample},{N_gap}")
        for i in range(0,int(len(self.y_filtered)),int(N_gap)):
            self.filter.y_resample.append(self.y_filtered[i])
            #ifprint(i)
        print(f"N_resampling: {len(self.filter.y_resample)}")

    def BG_subtract(self,signal,noise):
        """the input graph should have same x values"""
        return (signal-noise)
    def moving_avg(self,values,N_avg=1):
        values_return =np.zeros(len(values))
        for i in range(N_avg):
            values_return[i]=values[i]
            values_return[-1*(i+1)]=values[-1*(i+1)]
        for i in range(N_avg,len(values)-N_avg):
            values_return[i]=np.average(values[i-N_avg:i+N_avg+1])
        return values_return

class noise_model:
    '''
     
    This is the class to model the SiPM noise after irradiation:
    1/f noise with formula of A_0/f^gamma
    waveform response noise: platform roll-off at specific point
    
    '''
    #flicker noise  A0/f^gamma 
    f_noise_gamma = 2.              #gamma  dimensionless    
    f_noise_A0 = 0.                 #log10(A0)  unit: decade
    #SiPM response signal
    s_noise_level = -60.            #unit: dB
    s_noise_roll_off_point = 6.     #unit: decade
    s_noise_roll_off_speed = 16.5    #unit: dB/decade
    #parameters
    pars = np.zeros(5)
    #functions
    func_f_noise = nullptr
    func_s_noise = nullptr
    #def __init__(self,f_noise_gamma,f_noise_A0,s_noise_level,s_noise_roll_off_point,s_noise_roll_off_speed):
    def __init__(self,pars):
        '''
        PSD: dB
        f: decade
        '''
        if len(pars)==len(self.pars):
            self.pars = pars
            #self.pars[0]     = f_noise_A0
            #self.pars[1]     = f_noise_gamma
            #self.pars[2]     = s_noise_level
            #self.pars[3]     = s_noise_roll_off_point
            #self.pars[4]     = s_noise_roll_off_speed
            self.init_functions()
            self.update_pars()
        else: 
            print(f"ERROR: number of pars not corret, {len(self.pars)} needed!!")
    def init_functions(self):
        print(f"noise_model::init_functions...")
        self.func_f_noise = ROOT.TF1("func_f_noise","10.*([0]-[1]*x)",-2,8)
        self.func_s_noise = ROOT.TF1("func_s_noise","[0]+(x>[1])*[2]*(x-[1])",-2,8)
        self.func_f_noise.SetParNames(f"A_{{0}}","#gamma")
        self.func_s_noise.SetParNames("Platform_level",f"f_{{roll-off}}",f"Slope_{{roll-off}}")
        self.name_functions()

    def update_pars(self):
        self.func_f_noise.SetParameters(self.pars[:2])
        self.func_s_noise.SetParameters(self.pars[2:])
    
    def name_functions(self):
        self.func_f_noise.GetXaxis().SetTitle(f"Log_{{10}}(Frequency [Hz])")
        self.func_f_noise.GetYaxis().SetTitle(f"PSD [dB])")
        self.func_s_noise.GetXaxis().SetTitle(f"Log_{{10}}(Frequency [Hz])")
        self.func_s_noise.GetYaxis().SetTitle(f"PSD [dB])")
    def set_par(self,ID,value):
        '''
        0 => f_noise_A0                     #unit: decade        
        1 => f_noise_gamma                  #dimensionless
        2 => s_noise_level                  #unit: dB
        3 => s_noise_roll_off_point         #unit: decade
        4 => s_noise_roll_off_speed         #unit: dB/decade
        '''                                 
        self.pars[ID] = value
    def get_PSD_all(self,dB_unit=True):
        gr = ROOT.TGraph()
        gr = plot_helper.NameIt(gr,name="psd_all",title= "PSD all", xtitle=f"Log_{{10}}(Frequency [Hz])",ytitle="PSD [dB]")
        if not dB_unit:
            gr = plot_helper.NameIt(gr,ytitle=f"PSD [mV^{{2}}/Hz]")
        for f_log in np.arange(start=-2., step=0.1,stop=8.):
            psd = pow(10.,self.func_f_noise.Eval(f_log)/10.)+pow(10.,self.func_s_noise.Eval(f_log)/10.)
            if dB_unit:
                psd = 10.*np.log10(psd)
            gr.SetPoint(gr.GetN(),f_log,psd)
        return gr #TODO 
    def get_PSD_f_noise_function(self,dB_unit=True):
        '''noise psd follow 1/f^gamma'''
        return self.func_f_noise
    def get_PSD_s_noise(self,dB_unit=True):
        '''noise psd dominated by SiPM signal waveform'''
        return self.func_s_noise
    def cal_RMS_from_PSD(self,f_min,f_max,opt=0):
        '''
        f_xxx:
            unit: Hz
        opt:
            0 => all
            1 => 1/f like noise
            2 => SiPM response noise (DCR)
        '''
        rms_f_noise = self.cal_rms_f_noise(f_min,f_max)
        rms_s_noise = self.cal_rms_s_noise(f_min,f_max)
        rms_all = np.sqrt(rms_f_noise**2+rms_s_noise**2)

        if opt ==0:
            return rms_all    
        if opt ==1:
            return rms_f_noise    
        if opt ==2:
            return rms_s_noise    

    def cal_rms_f_noise(self,f_min,f_max):
        """
        This is the integral of the 1/f noise based on given parameters
        """
        A0 = pow(10.,self.pars[0])
        gamma = self.pars[1]
        return np.sqrt(A0/(1-gamma)*(pow(f_max,1-gamma)-pow(f_min,1-gamma)))

    def cal_rms_s_noise(self,f_min,f_max):
        """
        This is the integral of the SiPM response based on given parameters
        """
        a= self.pars[2]
        b= self.pars[3]
        c= self.pars[4]
        level  = pow(10.,a/10)
        f_roll = pow(10.,b)
        a1      = pow(10.,(a-b*c)/10.)
        b1      = c/10.+1.
        val_min = pow(f_min,b1)
        val_max = pow(f_max,b1)
        val_roll = pow(f_roll,b1)

        integral_start = (f_min<=f_roll)*f_min*level + (f_min>f_roll)*(level*f_roll+a1/b1*(val_min-val_roll))
        integral_stop = (f_max<=f_roll)*f_max*level + (f_max>f_roll)*(level*f_roll+a1/b1*(val_max-val_roll))
        return np.sqrt(integral_stop-integral_start) 
