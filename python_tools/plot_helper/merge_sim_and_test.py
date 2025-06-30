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
N_muon_sim =  1.577784e7    # Number of Muon used in the simulation  //This is for the simulation run "/media/archive/Data/irradiation/simulation/irradiation_setup/debug/beam_distribution_check/Run5"
Constant_scale_to_full =  proton_current_int*3600.*24*alpha /N_muon_sim
#==============================
#==============================
if(len(sys.argv)!=4 ):
    print(bc.ERROR+"Usage: ",sys.argv[0], " [file simulation] [file IV results] [file out]"+bc.ENDC)
    exit()
file_sim_name=sys.argv[1]
file_IV_name=sys.argv[2]
file_out_name=sys.argv[3]

if not Path(file_sim_name).is_file():
    print(f'{bc.ERROR}file {file_sim_name} does NOT exist!!{bc.ENDC}')
if not Path(file_IV_name).is_file():
    print(f'{bc.ERROR}file {file_IV_name} does NOT exist!!{bc.ENDC}')

file_IV = ROOT.TFile(file_IV_name)
gr_dark_current = file_IV.Get("HVconst/gr_Current_HV55_IV_mapping") #TGraph
gr_mapping = file_IV.Get("IV_scan_ch_mapping_to_sim")              #TGraph

gr_dark_current.Print()
gr_mapping.Print()

file_sim = ROOT.TFile(file_sim_name)
h_sim_dose = file_sim.Get("stat/Tiledose/Si/tilesipm_Si_NIELDose") #TH1D
h_sim_dose.Print()


file_out = ROOT.TFile(f"{file_out_name}.root","recreate")
file_out.cd()
gr_dark_current.Write()
gr_mapping.Write()
h_sim_dose.Write()

gr_I_vs_dose = ROOT.TGraph()
gr_I_vs_dose.SetNameTitle("Dark_Current_vs_dose_HV55V","Dark Current vs. NIEL Dose HV55V; NIEL dose [#times10^{11} 1 MeV n_{eq}/cm^2]; Dark current @55V [mA]")
for i in range(gr_dark_current.GetN()):
    I_tmp       = gr_dark_current.GetY()[i]*1000.   #unit:mA
    ch_sim      =  gr_mapping.Eval(gr_dark_current.GetX()[i])
    dose_tmp    = h_sim_dose.GetBinContent(h_sim_dose.FindBin(ch_sim))*Constant_scale_to_full/1.e11
    gr_I_vs_dose.SetPoint(gr_I_vs_dose.GetN(),dose_tmp,I_tmp)
gr_I_vs_dose.Write()

file_out.Close()
exit()

