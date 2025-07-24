import sys
from pathlib import Path
import math

import ROOT

sys.path.append("..")
from print_helper import bcolors 
bc=bcolors()
#==============================
#==============================
if(len(sys.argv)<7 ):
    print(bc.ERROR+"Usage: ",sys.argv[0], "[plot name 1] [plot name 2] [file1] [file2] [outfile name] [out type option: 0b(pdf)(png)(C)(root) default 0b1111]"+bc.ENDC)
    exit()
name1=sys.argv[1]
name2=sys.argv[2]
file1_name=sys.argv[3]
file2_name=sys.argv[4]
file_out_name=sys.argv[5]
option=int(sys.argv[6],2)
print(f'option {option}')
if not Path(file2_name).is_file():
    print(f'{bc.ERROR}file {file2_name} does NOT exist!!{bc.ENDC}')
    exit()
if not Path(file1_name).is_file():
    print(f'{bc.ERROR}file {file1_name} does NOT exist!!{bc.ENDC}')
    exit()

file1 = ROOT.TFile.Open(file1_name)
file2 = ROOT.TFile.Open(file2_name)
file1.Print()
file2.Print()

plt1_tmp = file1.Get(name1)
plt2_tmp = file2.Get(name2)
plt1 = ROOT.TGraph()
plt2 = ROOT.TGraph()
#for i in range(100):
#    plt1.SetPoint(plt1.GetN(),i,math.sqrt(i))
#    plt2.SetPoint(plt2.GetN(),i,math.pow(i,2))

y_min = 9999.
y_max = 0.
x_1_start =None
x_2_start =None
for i in range(100000):
    x_1=plt1_tmp.GetX()[i]
    y_1=plt1_tmp.GetY()[i]
    x_2=plt2_tmp.GetX()[i]
    y_2=plt2_tmp.GetY()[i]
    
    if i==0:
        x_1_start = x_1
        x_2_start = x_2
    plt1.SetPoint(plt1.GetN(),x_1-x_1_start,y_1)
    plt2.SetPoint(plt2.GetN(),x_2-x_2_start,y_2)
    y_min = (y_min,y_1)[y_1<y_min]
    y_min = (y_min,y_2)[y_2<y_min]
    y_max = (y_max,y_1)[y_1>y_max]
    y_max = (y_max,y_2)[y_2>y_max]

print(f"range: {y_min} {y_max}")
plt1.SetTitle("plot1; Time [ns]; Amplitude [mV]")
plt2.SetTitle("plot2; Time [ns]; Amplitude [mV]")

#set plot style
plt1.SetLineColor(ROOT.kBlack)
plt1.SetLineWidth(2)
plt1.SetMarkerColor(ROOT.kBlack)
plt1.GetYaxis().SetRangeUser(y_min*0.9,y_max*1.1)
#plt1.SetMarkerStyle(8)
#plt1.SetMarkerSize(2)

plt2.SetLineColor(ROOT.kRed)
plt2.SetLineWidth(2)
plt2.SetMarkerColor(ROOT.kRed)
plt2.GetYaxis().SetRangeUser(y_min*0.9,y_max*1.1)
#plt2.SetMarkerStyle(8)
#plt2.SetMarkerSize(2)

#check the type 
draw_opt1=""
draw_opt2=""
type1=type(plt1)
type2=type(plt2)
print(type1,type2)
if type1 is ROOT.TGraph:
    draw_opt1="APL"
elif type1 is ROOT.TGraphErrors:
    draw_opt1="APEL"
elif not (type1 is ROOT.TH1D):
    print(f'{bc.ERROR}plot1 is neither TGraph, TGraphErrors or TH1D. exist!!{bc.ENDC}')
    exit()
if type2 is ROOT.TGraph:
    draw_opt2="PL"
elif type2 is ROOT.TGraphErrors:
    draw_opt2="PEL"
elif not (type2 is ROOT.TH1D):
    print(f'{bc.ERROR}plot1 is neither TGraph, TGraphErrors or TH1D. exist!!{bc.ENDC}')
    exit()
draw_opt2 +=",same"
print(f'draw option: [{draw_opt1}] [{draw_opt2}]')

legend = ROOT.TLegend(0.65 ,0.7 ,0.85 ,0.9)
legend.AddEntry(plt1,"HV=0V")
legend.AddEntry(plt2,"HV=55V")
legend.SetLineWidth(0)

# create canvas
canvas=ROOT.TCanvas("canvas")
canvas.cd()
plt1.Draw(draw_opt1)
plt2.Draw(draw_opt2)
legend.Draw("same")

#save to files
#pdf
print("saving to PDF")
canvas.SaveAs(file_out_name+".pdf")
canvas.SaveAs(file_out_name+".C")
canvas.SaveAs(file_out_name+".png")

#root
file_out = ROOT.TFile(file_out_name+".root","recreate")
file_out.cd()
canvas.Write()
file_out.Close()

exit()
