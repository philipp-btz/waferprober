## Tiancheng Zhong
##This is the code to plot the RMS vs. dose

import sys
from pathlib import Path
import math
import numpy as np
from collections import OrderedDict

import ROOT

sys.path.append("..")
from print_helper import bcolors 
bc=bcolors()
proton_current_int = 20.28  # mADay
alpha = 6.99e7              # Muon/mADay
N_muon_sim =  1.577784e7    # Number of Muon used in the simulation
Constant_scale_to_full =  proton_current_int*3600.*24*alpha /N_muon_sim
#==============================
#==============================
if(len(sys.argv)!=4 ):
    print(bc.ERROR+"Usage: ",sys.argv[0], " [file simulation] [dir RMS spectrum] [file out]"+bc.ENDC)
    exit()
file_sim_name=sys.argv[1]
dir_RMS_name=sys.argv[2]
file_out_name=sys.argv[3]

if not Path(file_sim_name).is_file():
    print(f'{bc.ERROR}file {file_sim_name} does NOT exist!!{bc.ENDC}')
if not Path(dir_RMS_name).is_dir():
    print(f'{bc.ERROR}dir {dir_RMS_name} does NOT exist!!{bc.ENDC}')
gr_rms = ROOT.TGraph()
gr_mapping = ROOT.TGraph()

for matrix in range(1,8,1):
    for ch in range(16):
        file_IV = ROOT.TFile(f'{dir_RMS_name}/matrix{matrix}/RMS_results_ch{ch}.root')#TODO change it 
        gr_tmp = file_IV.Get("HVconst/gr_Current_HV55_IV_mapping") #TGraph
        print(f'N in graph: gr_tmp.GetN()')
        for index in range(gr_tmp.GetN()):
            gr_rms.SetPoint(gr_rms.GetN(),matrix*20+ch,gr_tmp.GetY()[index])
        gr_mapping = file_IV.Get("IV_scan_ch_mapping_to_sim")              #TGraph
gr_rms.SetNameTitle(f'RMS_in_local_ch',"RMS in different channels; Local ch ID [matrixID*20+chID]; RMS @55V on 50#Ohm [mV]")
gr_rms.Print()
gr_mapping.Print()

file_sim = ROOT.TFile(file_sim_name)
h_sim_dose = file_sim.Get("stat/Tiledose/Si/tilesipm_Si_NIELDose") #TH1D
h_sim_dose.Print()


file_out = ROOT.TFile(f"{file_out_name}.root","recreate")
file_out.cd()
gr_rms.Write()
gr_mapping.Write()
h_sim_dose.Write()

gr_I_vs_dose = ROOT.TGraph()
gr_I_vs_dose.SetNameTitle("RMS_vs_dose_HV55V","RMS vs. NIEL Dose HV55V; NIEL dose [#times10^{11} 1 MeV n_{eq}/cm^{2}]; RMS of signal @55V [mV]")
for i in range(gr_rms.GetN()):
    I_tmp       = gr_rms.GetY()[i] # change to current mV
    ch_sim      =  gr_mapping.Eval(gr_rms.GetX()[i])
    dose_tmp    = h_sim_dose.GetBinContent(h_sim_dose.FindBin(ch_sim))*Constant_scale_to_full/1.e11
    gr_I_vs_dose.SetPoint(gr_I_vs_dose.GetN(),dose_tmp,I_tmp)
gr_I_vs_dose.Write()

file_out.Close()
exit()

