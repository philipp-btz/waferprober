import sys
sys.path.append("..")
from plot_helper.pyroot_helper import root_helper as rt_hp

import ROOT
gr1 = ROOT.TH1D("h1","h1;X [mm];Y [a.u.]",1000,-5.,5.)
gr1.FillRandom("gaus",1000)
gr2 = ROOT.TH1D("h2","h2;X [mm];Y [a.u.]",1000,-5.,5.)
gr2.FillRandom("gaus",1000)
can=rt_hp.Draw_2_plt_ratio(gr=gr1,gr_base=gr2)
file_out=ROOT.TFile("results_test_plot_helper.root","recreate")
file_out.cd()
can.Write()
can.Print("results_test_plot_helper.pdf")
file_out.Close()
exit()
