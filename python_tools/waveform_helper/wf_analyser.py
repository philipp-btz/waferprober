
import ROOT

import numpy as np
import ctypes
from scipy.signal import find_peaks, savgol_filter

##  Tiancheng Zhong
##  20210824
## This is the class mainly used for SiPM waveform analysis
class wf_ana:
    DEBUG=True
    def __init__(self,gr,sample_gap=0.05, part=1.0):
        if gr.GetN()>0:
            self.gr = gr        #data with form of ROOT.TGraph
            self.x = np.asarray(gr.GetX())
            self.y = np.asarray(gr.GetY())
            self.N = len(self.y)
            self.part = part
            self.time = self.x[self.N-1]-self.x[0]
            self.sample_gap = sample_gap    # unit:ns
            self.EN_level = 5. # this might be different from different measurement
            self.PE_level = 30. # single photon level
            self.nPeaks = 0
            self.indexPeaks = []
            self.th1 = None
            self.y_smooth = []
    #==================transfer TGraph to TH1D======
    def gen_th1(self,Smooth=False):  
        print("Generating TH1D for WF...")
        self.th1 = ROOT.TH1D("h","h",int(self.N*self.part),self.x[0],self.x[0]+self.part*(self.x[self.N-1]-self.x[0]))
        if Smooth and len(self.y_smooth)==0:
            print("gen_th1(): TGraph is not smooth yet")
        for bin in range(int(self.N*self.part)):
            if Smooth:
                self.th1.SetBinContent(bin,self.y_smooth[bin])
            else:
                self.th1.SetBinContent(bin,self.y[bin])

        print("done")
    #==================return the Th1D=====
    def get_th1(self):
        if self.th1==None:
            self.gen_th1()
        return self.th1
    #==================return the Th1D=====TODO: currently only check part of the histogram
    def get_peaks(self):
        if self.th1 ==None:
            self.gen_th1(True)
        print("searching for peaks...")
        spc = ROOT.TSpectrum()
        #nfound = spc.Search(self.th1,10 ,"",threshold=0.4)
        source = self.y[0:int(self.N*self.part)]
        dest = np.ndarray((len(source),),dtype=np.double)
        
        nfound = spc.SearchHighRes(source,dest , len(source), 5, 40, True, 3, True, 3);
        print(f'{nfound} peaks found!')
        if nfound<1:
            return -1
        gr_peaks = ROOT.TGraph()
        for i in range(nfound):
            gr_peaks.SetPoint(i,spc.GetPositionX()[i],spc.GetPositionY()[i])
        if self.DEBUG:
            gr_dest =ROOT.TGraph()
            gr_dest =ROOT.TGraph(len(dest),self.x[0:len(dest)],dest)
            gr_dest.SetNameTitle("dest","dest; Time [ns]; Amplitude [mV]")
            return gr_peaks,gr_dest
        return gr_peaks
    #==================count the event above the thr[thr: number or array]=====
    def cal_cnt(self,thr,tolerence=0.7):
        #TODO this can be done with shift of a array
        if type(thr)!=np.ndarray:
            try:
                thr = np.asarray([thr])
            except:
                print(f'There is something wrong with the thr')
                return -1
        cnt = np.zeros(len(thr))
        Abv_thr = [False for i in range(len(thr))]
        print(cnt,Abv_thr)
        P_found = False
        for iPoint in range(self.N):
            if iPoint%10000 ==0:
                print(f'analysising {iPoint:.2e} [{iPoint/self.N*100:.2f}%]...')
            if iPoint/self.N >self.part:
                break
            if self.y[iPoint]<thr[0]*tolerence:
                Abv_thr[0] = False
                continue
            for iThr in range(len(thr)):
                if Abv_thr[iThr]==True and self.y[iPoint]<thr[iThr]*tolerence:
                    Abv_thr[iThr] = False
                    continue
                if Abv_thr[iThr]==False and self.y[iPoint]>thr[iThr]:
                    cnt[iThr]+=1
                    Abv_thr[iThr] = True
                    continue
                #print(f'iThr {iThr}')
        return thr,cnt
    #==================Check the density of different values=====
    def get_y_count(self,thr=None):
        h1d = ROOT.TH1D("h1d","h1d",100,round(np.amin(self.y)),round(np.amax(self.y)))
        for i in range(self.N):
            if i%10000 ==0:
                print(f'analysising {i:.2e} [{i/self.N*100:.2f}%]...')
            if i/self.N >self.part:
                break
            h1d.Fill(self.y[i])
        return h1d
    #==================Draw transparent waveform with given thr=====
    def draw_overload_plots(self, thr, time_pre=5., time_post=50.):
        cnt_unit_time = int(1./self.sample_gap)
        n_triggered =0
        h2d = ROOT.TH2D("h2d","h2d",int((time_post+time_pre)/self.sample_gap),-time_pre,time_post,100,round(np.amin(self.y)),round(np.amax(self.y)))
        
        for i in range(int(time_pre/self.sample_gap),self.N-int(time_post/self.sample_gap)):
            if i%10000 ==0:
                print(f'analysising {i:.2e} [{i/self.N*100:.2f}%]...')
            if i/self.N >self.part:
                break
            if self.y[i]<thr:
                continue
            if self.y[i-1]<thr and self.y[i]>thr and np.mean(self.y[i-cnt_unit_time:i])<np.mean(self.y[i:i+cnt_unit_time]) and  np.mean(self.y[i-2*cnt_unit_time:i-cnt_unit_time])< self.EN_level and np.mean(self.y[i+cnt_unit_time:i+2*cnt_unit_time]>self.EN_level): # triggered
                for ii in range(int(-time_pre/self.sample_gap),int(time_post/self.sample_gap)):
                    h2d.Fill(self.x[i+ii]-self.x[i],self.y[i+ii])
                i+=time_post/self.sample_gap
                n_triggered +=1
        print(f"triggered {n_triggered} times")
        return h2d

        
        
    #================== get dt distribution of given thr ======
    def get_dt(self,thr,res_up):# smooth the wf and get the time stamp at fiven thr;
        h1d = ROOT.TH1D("h1d","h1d",200,0,20000.)
        gr = self.get_time(thr,res_up)[0]
        for index in range(1,gr.GetN()):
            h1d.Fill(gr.GetX()[index]-gr.GetX()[index-1])
        return h1d
    #================== get the TGraph of time triggered at given thr ======
    def get_time(self,thr,res_up):# smooth the wf and get the time stamp at given thr; 
        thr_up = thr + res_up
        time = 5.       #ns
        self.avg_wf(int(time/2./self.sample_gap)*2+1)
        thr_bool = (self.y_smooth>thr)
        thr_up_bool = (self.y_smooth>thr_up)
        if self.DEBUG:
            gr1 = ROOT.TGraph(len(thr_bool),self.x,thr_bool*thr)
            gr2 = ROOT.TGraph(len(thr_up_bool),self.x,thr_up_bool*thr_up)
        gr_t = ROOT.TGraph()
        gr_t.SetNameTitle("gr_time_stamp","Time stamp; Time [ns]; Amplitude [mV]")
        index_last = 0
        print(f"n {len(thr_bool)}; n_up {len(thr_up_bool)}")
        for index in range(1,len(thr_bool)):
            if thr_up_bool[index] and thr_up_bool[index-1]==False:
                index_curr =  index
                while index_curr>0:
                    if thr_bool[index_curr] and thr_bool[index_curr-1]==False:
                        if index_curr!=index_last:
                            gr_t.SetPoint(gr_t.GetN(),self.x[index_curr],thr)
                            index_last = index_curr
                        break
                    index_curr -=1
        if self.DEBUG:
            return gr_t,gr1,gr2
        else:
            return gr_t 
    
    
    #================== Average wf with Savitzky-Golay filter ======
    def avg_wf(self,n_avg,polyorder=0,bool_return=False): #1:normal; 2:moving avg smooth wf
        self.y_smooth = savgol_filter(self.y[0:int(self.N*self.part)],n_avg,polyorder)
        gr=ROOT.TGraph(int(self.N*self.part),self.x,self.y_smooth)
        gr.SetNameTitle(f"wf_smooth_Navg{n_avg}_poly{polyorder}",f"wf_smooth_Navg{n_avg}_poly{polyorder}; Time [ns]; Amplitude [mV]")
        return gr
    
    #================== get the peak location of wf ====== 
    def get_peak_location(self,x_distance,Y_delta): # this is the all the extrame value and the peak of the signal is included 
        if len(self.y_smooth)==0:
            avg_time = 5.  #ns
            self.avg_wf(int(avg_time/2./self.sample_gap)*2+1)
        gr_good_peaks = ROOT.TGraph()
        gr_good_peaks.SetName("good_peaks")
        gr_peaks = ROOT.TGraph()
        gr_peaks.SetName("peaks")
        gr_start_mark = ROOT.TGraph()
        gr_start_mark.SetName("Start_marker")
        gr_stop_mark  = ROOT.TGraph()
        gr_stop_mark.SetName("Stop_marker")
        gr_trig_stat = ROOT.TGraph()
        gr_trig_stat.SetName("trigger_status")
        th1_ap_cnt = ROOT.TH1D("AP_hist","AP_hist; Number of peaks; Entries",5,0,5) 
        #check signal range
        thr_bool_high   = (self.y_smooth>self.PE_level*0.6) 
        thr_bool_low    = (self.y_smooth>self.PE_level*0.4) 
        gr_bool_high = ROOT.TGraph(len(thr_bool_high),self.x,thr_bool_high*self.PE_level*0.6)
        gr_bool_low = ROOT.TGraph(len(thr_bool_low),self.x,thr_bool_low*self.PE_level*0.4)
        signal_bool = [False]*len(thr_bool_low)
        signal_range = []
        triggered = False
        start_index =-1
        for i in range(len(thr_bool_low)):
            if thr_bool_low[i] ==False:
                continue
            else:
                if thr_bool_high[i]==False and thr_bool_high[i+1] and triggered==False: #higher bool: shift from low to high
                    start_index = i
                    triggered = True
                    gr_start_mark.SetPoint(gr_start_mark.GetN(),self.x[i],self.y_smooth[i])
                if thr_bool_low[i] and thr_bool_low[i+1]==False and triggered==True: #lower bool: shift from high to low
                    signal_range.append((start_index,i))
                    gr_stop_mark.SetPoint(gr_stop_mark.GetN(),self.x[i],self.y_smooth[i])
                    triggered = False
            gr_trig_stat.SetPoint(gr_trig_stat.GetN(),self.x[i],triggered*self.PE_level*0.6) 
        # check max point 
        for (index_start,index_stop)  in signal_range:
            peaks_index =find_peaks(self.y_smooth[index_start:index_stop],height=0.5*self.PE_level,distance=int(x_distance/self.sample_gap))[0]+index_start
            print(f"total peaks: {len(peaks_index)}")
            
            for index in peaks_index:
                gr_peaks.SetPoint(gr_peaks.GetN(),self.x[index],self.y_smooth[index])

            if len(peaks_index)<1:
                continue
            if len(peaks_index)==1:
                gr_good_peaks.SetPoint(gr_good_peaks.GetN(),self.x[peaks_index[0]],self.y_smooth[peaks_index[0]])
                th1_ap_cnt.Fill(1.)
                print(f"Number of good peaks: 1")
                continue
            if len(peaks_index)>1: #check after pulse exist or not
                peaks_good_index =[]
                peak_max_index = peaks_index[0]
                peak_max_index_index = 0
                for i in range(len(peaks_index)):
                    if self.y_smooth[peaks_index[i]]>self.y_smooth[peak_max_index]:
                        peak_max_index = peaks_index[i]
                        peak_max_index_index = i
                peaks_good_index.append(peak_max_index) # main peak

                if(peak_max_index_index!=0): #check peaks on the LEFT side of the main peak
                    last_peak_index = peak_max_index
                    for i in range(peak_max_index_index-1,-1,-1):
                        #print(f"check left: ID {i}")
                        if peaks_index[i]>=last_peak_index:
                            continue
                        vallay_index = np.argmin(self.y_smooth[peaks_index[i]:last_peak_index+1])+peaks_index[i]
                        
                        if self.y_smooth[last_peak_index]-self.y_smooth[vallay_index]>Y_delta and self.y_smooth[peaks_index[i]]-self.y_smooth[vallay_index]>Y_delta:
                            if i==0:
                                peaks_good_index.append(peaks_index[0]) #finish search if this is already the first peak
                                break
                            for ii in range(1,i+1):
                                vallay_index2 = np.argmin(self.y_smooth[peaks_index[i-ii]:peaks_index[i]+1])+peaks_index[i-ii]
                                if self.y_smooth[peaks_index[i]]-self.y_smooth[vallay_index2]>Y_delta and self.y_smooth[peaks_index[i-ii]]-self.y_smooth[vallay_index2]>Y_delta:
                                    if ii==1:
                                        peaks_good_index.append(peaks_index[i])
                                        last_peak_index = peaks_index[i]
                                    else:
                                        last_peak_index = np.argmax(self.y_smooth[peaks_index[i-ii+1]:peaks_index[i]+1])+peaks_index[i-ii+1]
                                        peaks_good_index.append(last_peak_index)
                                    break
                                elif i-ii == 0:
                                    last_peak_index = np.argmax(self.y_smooth[peaks_index[i-ii]:peaks_index[i]+1])+peaks_index[0]
                                    peaks_good_index.append(last_peak_index)
                                    break
                 
                if(peak_max_index_index!=len(peaks_index)-1): #check peaks on the RIGHT side of the main peak
                    last_peak_index = peak_max_index
                    for i in range(peak_max_index_index+1,len(peaks_index),1):
                        #print(f"check right: ID {i}")
                        if peaks_index[i]<last_peak_index:
                            continue
                        vallay_index = np.argmin(self.y_smooth[last_peak_index:peaks_index[i]+1])+last_peak_index
                        
                        if self.y_smooth[last_peak_index]-self.y_smooth[vallay_index]>Y_delta and self.y_smooth[peaks_index[i]]-self.y_smooth[vallay_index]>Y_delta:
                            #print(f"vallay found between last_peak and {i}")
                            if i==len(peaks_index)-1:
                                peaks_good_index.append(peaks_index[len(peaks_index)-1]) #finish search if this is already the first peak
                                break
                            for ii in range(1,len(peaks_index)-i): 
                                #print(f"check {i} is peak or  not... {ii}")
                                vallay_index2 = np.argmin(self.y_smooth[peaks_index[i]:peaks_index[i+ii]+1])+peaks_index[i]
                                if self.y_smooth[peaks_index[i]]-self.y_smooth[vallay_index2]>Y_delta and self.y_smooth[peaks_index[i+ii]]-self.y_smooth[vallay_index2]>Y_delta:
                                    if ii==1:
                                        peaks_good_index.append(peaks_index[i])
                                        last_peak_index = peaks_index[i]
                                    else:
                                        last_peak_index = np.argmax(self.y_smooth[peaks_index[i]:peaks_index[i+ii-1]+1])+peaks_index[i]
                                        peaks_good_index.append(last_peak_index)
                                    break
                                elif ii+i == len(peaks_index)-1:
                                    last_peak_index = np.argmax(self.y_smooth[peaks_index[i]:peaks_index[i+ii]+1])+peaks_index[i]
                                    peaks_good_index.append(last_peak_index)
                                    break

                print(f"Number of good peaks: {len(peaks_good_index)}")
                peaks_good_index = np.sort(peaks_good_index)
                th1_ap_cnt.Fill(len(peaks_good_index))
                for index in peaks_good_index:
                    gr_good_peaks.SetPoint(gr_good_peaks.GetN(),self.x[index],self.y_smooth[index])
        if self.DEBUG:
            return gr_good_peaks,th1_ap_cnt,gr_peaks, gr_start_mark,gr_stop_mark, gr_bool_high,gr_bool_low,gr_trig_stat 
        return gr_good_peaks,th1_ap_cnt
            
    #================== get back waveform ====== 
    def get_wf(self,Smooth=False):
        values = self.y[0:int(self.N*self.part)]
        name = "Waveform"
        if Smooth:
            if len(self.y_smooth)==0:
                print("wf is not smoothed yet!")
                return -1
            values = self.y_smooth
            name +="_smooth"
        gr = ROOT.TGraph(len(values),self.x,values)
        gr.SetNameTitle(f"{name}",f"{name}; Time [ns]; Amplitude [mV]")
        return gr 
    

    def cal_slope_and_time_along_thr(self,gr_wf,thr_array,upper_thr):
        '''
        gr_wf: wf with TGraph form
        thr_array: threshold aray
        upper_thr: maximum y in gr_wf you are interested the data higerh than this will be throw away
        return:  the corresponding [slope] and [time stamp] at given threshold [thr_array]
        '''
        time = np.asarray(gr_wf.GetX())
        amp  = np.asarray(gr_wf.GetY())

        #cut away values higher than upper_thr
        index_cut = np.argmax(amp>upper_thr)
        #print("index_cut:",index_cut,"thr_upper",upper_thr)
        time = time[:index_cut]
        amp = amp[:index_cut]

        # reverse array  :: leading edge chagned to decaying edge
        time = time[::-1]
        amp  = amp[::-1]
        # loop over the waveform and get the timestamp and slope
        n_thr = len(thr_array)
        slope_thr = np.full(n_thr,-999.)
        time_thr = np.full(n_thr,-999.)
        for index_thr in range(len(thr_array)): # loop over threshold
            thr = thr_array[index_thr]
            index_found = -1
            for index in range(len(amp)-1): # loop over 
                if amp[index]>thr and amp[index+1]<=thr:
                    index_found = index
                    break
            if index_found<0:
                continue
            slope_thr[index_thr] = (amp[index]-amp[index+1])/(time[index]-time[index+1])
            time_thr[index_thr] = time[index] + (thr-amp[index])/slope_thr[index_thr]
        return slope_thr,time_thr