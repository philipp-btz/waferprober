from matplotlib.style import use
import numpy as np
import ROOT
import sys

if __name__ == "__main__":
    '''
    Pre-analysis for the annealing study. Creates a TGraphErrors for the temperature across multiple IV-scans.
    '''
    if(len(sys.argv)!=3):
        print("Usage: ",sys.argv[0], " [filein_name] [output file name]")
        exit()        
    infile = sys.argv[1]
    outfile = sys.argv[2]
    x = np.loadtxt(infile,dtype=float,usecols=0)
    y = np.loadtxt(infile,dtype=float,usecols=1)
    ex = np.zeros(len(x))
    ey = np.full((1,len(x)),0.2)
    print(x,y)
    gr_T = ROOT.TGraphErrors(len(x),x,y,ex,ey)
    gr_T.SetNameTitle("T_allRuns","Temperature across different runs")
    gr_T.GetXaxis().SetTitle("runID")
    gr_T.GetYaxis().SetTitle(f"Temperature [C#circ]")
    gr_T.SetLineWidth(3)
    #save to root file
    root_file = ROOT.TFile(f"{outfile}.root","recreate")
    root_file.cd()
    gr_T.Write()
    root_file.Close()
    #save to png file
    canvas_png = ROOT.TCanvas("T_allRuns","T_allRuns",900,600)
    canvas_png.cd()
    gr_T.Draw("apl")
    canvas_png.SaveAs(f"{outfile}.png")
    exit()