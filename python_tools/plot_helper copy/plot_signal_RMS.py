##Tiancheng 2021.07
## This is used to plot the  results from IV scan

import sys
from pathlib import Path
import math
import numpy as np
from collections import OrderedDict

import ROOT

sys.path.append("..")
from print_helper import bcolors 
bc=bcolors()

runID = np.asarray([3,7,8,9,6,5,4,2]) # index is the matrix ID; value is the runID
ch_to_UID=np.asarray([9,4,15,13,12,14,8,10,2,11,7,0,1,3,6,5])  #index is the local channel and the value is UID
dict_matrix_to_runID=OrderedDict()

def gr_ZeroCorr(gr):
    n= gr.GetN()
    x = np.asarray(gr.GetX())
    y = np.asarray(gr.GetY())-gr.GetY()[0]
    return ROOT.TGraph(n,x,y)

def ch_map_to_simulation(dir_name):
    ch_mapping_file = open(f"{dir_name}/ch_mapping_to_sim.text",'w')
    ch_mapping_file.write("(matrixID,Local ID) => (x,y) => simID\n")
    for matrix in range(1,7,1):
        for LocID in range(16):
            if matrix>=4 and matrix<7:
                y=ch_to_UID[LocID]//4+(matrix-4)*4
                x=ch_to_UID[LocID]%4+4
            elif matrix<4 and matrix>0:
                y=3-ch_to_UID[LocID]//4 + (matrix -1)*4
                x=3-ch_to_UID[LocID]%4
            else:
                continue
            ch_mapping_file.write(f'({matrix},{LocID}) => ({x},{y}) => {x+y*8}\n')
def get_ch_in_sim(matrix,LocID,opt=1): #opt=1l return channel in Simulation; opt=2: return x,y coordination in siulation
    if matrix>=4 and matrix<7:
        y=ch_to_UID[LocID]//4+(matrix-4)*4
        x=ch_to_UID[LocID]%4+4
    elif matrix<4 and matrix>0:
        y=3-ch_to_UID[LocID]//4 + (matrix -1)*4
        x=3-ch_to_UID[LocID]%4
    else:
        return -1
    
    if opt==1:
        return x+y*20
    elif opt==2:
        return x,y
    else:
        print(f"get_ch_in_sim:: option {opt} is not defined!!")
        return -1
def getRMS_along_HV(file_name):
    file_tmp = ROOT.TFile(file_name)
    gr_RMS = ROOT.TGraph()
    for hv in range(52000,56000,200):
        print("hv: ",hv)
        gr_tmp = file_tmp.Get(f"WF_ch2_HV{hv}mV_index0")
        if gr_tmp.GetN()<1:
            print(f'{bc.ERROR} TGraph WF_ch2_HV{hv}mV_index0 does NOT exist!!{bc.ENDC}')
            continue
        rms_tmp = gr_tmp.GetRMS(2)
        hv_corr = gr_tmp.GetMean(2)/50.*1000.
        print("RMS: ",rms_tmp)
        gr_RMS.SetPoint(gr_RMS.GetN(),(hv-hv_corr)/1000.,rms_tmp)
        #free(gr_tmp)
    file_tmp.Close() 
    gr_RMS.SetNameTitle(f"IV_Scan_matrix{iMatrixID}_ID{LocID}",f"IV curve (matrix{iMatrixID}, CH{LocID}); HV [V]; RMS [mV]")
    return gr_RMS
#==============================
#==============================
if(len(sys.argv)!=5 ):
    print(bc.ERROR+"Usage: ",sys.argv[0], " [dir_name] [output file name] [ch] [matrix] "+bc.ENDC)
    #print(bc.ERROR+"Usage: ",sys.argv[0], " [dir_name] [output file name]"+bc.ENDC)
    exit()
dir_name=sys.argv[1]
file_out_name=sys.argv[2]
ch_interested=int(sys.argv[3])
matrix_interested = int(sys.argv[4])

######test####
ch_map_to_simulation(dir_name)
get_ch_in_sim(3,3)
get_ch_in_sim(7,2)

gr_ch = ROOT.TGraph()
for matrix in range(8):
    for LocID in range(16):
        if matrix<7 and matrix>0:
            gr_ch.SetPoint(gr_ch.GetN(),matrix*20+LocID,get_ch_in_sim(matrix,LocID))
        else:
            gr_ch.SetPoint(gr_ch.GetN(),matrix*20+LocID,-1)

gr_ch.SetNameTitle("IV_scan_ch_mapping_to_sim","IV Scan channel mapping to simulation channel; Ch ID in IV scan; Ch ID in simulation")

###########

file_out = ROOT.TFile(f"{dir_name}/{file_out_name}_ch{ch_interested}.root","recreate")
gr_ch.Write()

dir_RMSplot = file_out.mkdir("RMSplot/")
dir_HVconst = file_out.mkdir("HVconst/")

#grs to get 
grs_HVconst = []   # index+54 is thehv
grs_HVconst_UIDmapping = []  # index+54 is thehv
hs_HVconst = []  # index+54 is thehv
for index in range(5):
    grs_HVconst.append(ROOT.TGraph() )
    grs_HVconst_UIDmapping.append(ROOT.TGraph())
    hs_HVconst.append(ROOT.TH2D(f"h_{index}","h",8,0,8,12,0,12))


for LocID in [ch_interested]:
    print("localID",LocID)
    grs = []
    grs_corr = []
    for iMatrixID in [matrix_interested]:
        print("matrix: ",iMatrixID)
        file_name = f'{dir_name}/matrix{iMatrixID}/scope_Beam_signal_run{runID[iMatrixID]}_DUT_matrix{iMatrixID}_ch{LocID}_T11.0_1wf_SR20GHz.root'
        if not Path(file_name).is_file():
            print(f'{bc.ERROR}file {file_name} does NOT exist!!{bc.ENDC}')
            continue
        gr_RMS=getRMS_along_HV(file_name)
        dir_RMSplot.cd()
        gr_RMS.Write()
        grs_corr.append(gr_RMS)#TODO check TGraph exist or not

        
        for index in range(5): #get the RMS of different channels 
            grs_HVconst_UIDmapping[index].SetPoint(grs_HVconst_UIDmapping[index].GetN(),iMatrixID*20+ch_to_UID[LocID],gr_RMS.Eval(index+52))
            if iMatrixID<7 and iMatrixID>0:#mapping to simulation channel
                grs_HVconst[index].SetPoint(grs_HVconst[index].GetN(),get_ch_in_sim(iMatrixID,LocID),gr_RMS.Eval(index+52))
                x,y =get_ch_in_sim(iMatrixID,LocID,2)
                hs_HVconst[index].Fill(8-(x+0.5),y+0.5,gr_RMS.Eval(index+52))
    
    canvas1=ROOT.TCanvas(f"IV_curve_UID{ch_to_UID[LocID]}")
    canvas1.cd()
    legend1 = ROOT.TLegend(0.15 ,0.5 ,0.35 ,0.9)
    legend1.SetLineWidth(0)
    legend1.SetFillStyle(0)
    for i in range(len(grs_corr)):
        if i==0:#add all the matrix which you don't want to draw
            continue 
        legend1.AddEntry(grs_corr[i],f"Matrix{i} UID{ch_to_UID[LocID]}")
        canvas1.cd()
        if i==1:
            grs_corr[i].Draw("APL")
            #grs_corr[i].GetYaxis().SetRangeUser(1.e-8,2.e-3)
            #grs_corr[i].GetXaxis().SetRangeUser(48,58.2)
        else:
            grs_corr[i].Draw("samepl plc pmc")
        dir_RMSplot.cd()
        grs_corr[i].Write()
    if legend1.GetNRows() <1:
        continue
    canvas1.SetLogy(True)
    canvas1.cd()
    legend1.Draw("same")
    if ch_to_UID[LocID]==9:
        canvas1.SaveAs(f"{dir_name}/{file_out_name}_UID{ch_to_UID[LocID]}.pdf")
        canvas1.SaveAs(f"{dir_name}/{file_out_name}_UID{ch_to_UID[LocID]}.png")
        canvas1.SaveAs(f"{dir_name}/{file_out_name}_UID{ch_to_UID[LocID]}.C")
    
    dir_RMSplot.cd()
    canvas1.Write()

#save data where HV is constant
dir_HVconst.cd()
for index in range(len(grs_HVconst)):
    grs_HVconst[index].SetNameTitle(f"gr_Current_HV{52+index}",f"Dark Current HV={52+index}V; Ch ID in simulation; RMS [mV]")
    grs_HVconst_UIDmapping[index].SetNameTitle(f"gr_Current_HV{52+index}_IV_mapping",f"Dark Current HV={52+index}V; UID on PCB; RMS [mV]")
    hs_HVconst[index].SetNameTitle(f"h2d_Current_HV{52+index}",f"Dark Current HV={52+index}V; Ch ID along x; Ch ID along y; RMS [mV]")
    grs_HVconst[index].Write()   
    grs_HVconst_UIDmapping[index].Write()   
    hs_HVconst[index].Write()   

file_out.Close()
exit()

