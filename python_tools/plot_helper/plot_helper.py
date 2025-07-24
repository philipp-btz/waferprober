
import numpy as np
import ROOT

class plot_helper:
    pads=[]
    legends=[]
    canvas=0 
    def __init__(self) -> None:
        pass
    
    def __init__(self,canvas_name="canvas",n_x=1,n_y=2):
        self.init_canvas(canvas_name,n_x,n_y)
    
    def init_canvas(self,canvas_name="canvas",n_x=1,n_y=2,x_fraction=0.5,y_fraction=0.3):
        self.canvas=ROOT.TCanvas(canvas_name)
        if n_x==1 and n_y==2:
            self.pads.append(ROOT.TPad("pad1","pad1",0,y_fraction,1,1))
            self.pads.append(ROOT.TPad("pad2","pad2",0,0.05,1,y_fraction))
            #self.legends.append(ROOT.TLegend("pad1","pad1",0,y_fraction,1,1))
            #self.legends.append(ROOT.TLegend("pad2","pad2",0,0.05,1,y_fraction))
        if n_x==2 and n_y==1:
            self.pads.append(ROOT.TPad("pad1","pad1",0,0.05,x_fraction,1))
            self.pads.append(ROOT.TPad("pad2","pad2",x_fraction,0.05,1,1))

    def reset(self):
        self.canvas=0
        self.pads=[]
        self.legends=[]
    def NameIt(self,obj,name=0,title=0,xtitle=0,ytitle=0):
        if name==0 and title==0 and xtitle==0 and ytitle==0:
            print("ARE U serious? give some parameter to NameIt()")
        if name:
            obj.SetName(name)
        if title:
            obj.SetTitle(title)
        if xtitle:
            obj.GetXaxis().SetTitle(xtitle)
        if ytitle:
            obj.GetYaxis().SetTitle(ytitle)
        return obj
    def add_plot(self,obj,ipad=0,color=1,line_style=9,marker_size=0,marker_style=8,bool_edit=True):
        self.pads[ipad].cd()
        if bool_edit:
            obj.SetTitle("")
            obj.SetLineColor(color)
            obj.SetLineStyle(line_style)
            obj.SetMarkerStyle(marker_style)
            obj.SetMarkerSize(marker_size)
        obj.Draw("same")
        return self.canvas
    def draw_2_plts_UD(self,gr,gr_base,canvas_name="canvas",legend1="gr",legend2="gr_base",
    LogY=False,LogX=False,
    GridY=True,GridX=True,
    y1_range=[],y2_range=[],
    y1_Ndiv=0,y2_Ndiv=0
    ):
        self.init_canvas(canvas_name=canvas_name)
        
        self.canvas.cd()
        #pad 1
        self.pads[0].SetBottomMargin(0)
        self.pads[0].SetLogy(LogY)
        self.pads[0].SetLogx(LogX)
        self.pads[0].Draw()
        self.pads[0].cd()
        gr.SetTitle("")
        gr.GetXaxis().SetLabelSize(0)
        gr.GetXaxis().SetTitleSize(0)
        gr.GetYaxis().SetTitleSize (0.05)
        if len(y1_range)>0:
            gr.GetYaxis().SetRangeUser(y1_range[0],y1_range[1])
        if y1_Ndiv>0:
            gr.GetYaxis().SetNdivisions(y1_Ndiv)

        gr.Draw()
        
        self.canvas.cd()
        #pad 2
        self.pads[1].SetTopMargin(0)
        self.pads[1].SetBottomMargin(0.3)
        self.pads[1].Draw()
        self.pads[1].cd()
        gr_base.SetTitle("")
        gr_base.GetXaxis().SetLabelSize (0.15)
        gr_base.GetXaxis().SetTitleSize (0.15)
        gr_base.GetYaxis().SetLabelSize (0.15)
        gr_base.GetYaxis().SetTitleSize (0.15)
        gr_base.GetYaxis().SetTitleOffset (0.3)
        gr_base.GetXaxis().SetTitleOffset (0.9)
        if len(y2_range)>0:
            gr_base.GetYaxis().SetRangeUser(y2_range[0],y2_range[1])
        if y2_Ndiv>0:
            gr_base.GetYaxis().SetNdivisions(y2_Ndiv)
        gr_base.Draw()

        #legends
        legend= ROOT.TLegend(0.7 ,0.6 ,0.85 ,0.75)
        legend.AddEntry(gr ,legend1)
        legend.AddEntry(gr_base ,legend2)
        legend.SetLineWidth (0)
        legend.Draw("same")

        # Latex 
        #latex = ROOT.TLatex ()
        #latex.SetNDC()
        #latex.SetTextSize(0.06)
        #latex.DrawText(0.7 ,0.83 , " HASCO 2018 ")
        #latex.SetTextSize(0.04)
        #latex.DrawText(0.7 ,0.77 , "Di - muon events ")
        
        return self.canvas
    def cal_ratio_gr_to_f_fit(self,gr,f_fit):
        gr_ratio=ROOT.TGraphErrors()
        bool_with_errors=False
        if type(gr) is ROOT.TGraphErrors:
            bool_with_errors=True
        n= gr.GetN()
        x=np.asarray(gr.GetX())
        y=np.asarray(gr.GetY())
        x_Err=np.zeros(n)
        y_Err=np.zeros(n)
        if bool_with_errors:
            x_Err = gr.GetEX()
            y_Err = gr.GetEY()
        for i in range(n):
            r_curr=y[i]/f_fit.Eval(x[i])
            Er_curr=y_Err[i]/f_fit.Eval(x[i])
            gr_ratio.SetPoint(gr_ratio.GetN(),x[i],r_curr)
            gr_ratio.SetPointError(gr_ratio.GetN()-1,x_Err[i],Er_curr[i])
        return gr_ratio

    def cal_diff_gr_to_f_fit(self,gr,f_fit,bool_norm=True,bool_percentage=True):
        gr_diff=ROOT.TGraphErrors()
        bool_with_errors=False
        if type(gr) is ROOT.TGraphErrors:
            bool_with_errors=True
        n= gr.GetN()
        x=np.asarray(gr.GetX())
        y=np.asarray(gr.GetY())
        x_Err=np.zeros(n)
        y_Err=np.zeros(n)
        if bool_with_errors:
            x_Err = gr.GetEX()
            y_Err = gr.GetEY()
        
        for i in range(n):
            y_fit = f_fit.Eval(x[i])
            diff_curr=y[i]-y_fit
            diffE_curr=y_Err[i]
            #print(y[i],y_fit,diff_curr)
            if bool_norm:
                diff_curr =  diff_curr/y_fit
                diffE_curr = diffE_curr/y_fit
                if bool_percentage:
                    diff_curr =  diff_curr*100.
                    diffE_curr = diffE_curr*100.
            #print(diff_curr)
            gr_diff.SetPoint(gr_diff.GetN(),x[i],diff_curr)
            gr_diff.SetPointError(gr_diff.GetN()-1,x_Err[i],diffE_curr)
        return gr_diff
    def get_R2(self, gr,f):
        x= np.asarray(gr.GetX())
        y= np.asarray(gr.GetY())
        y_mean = gr.GetMean(2)
        sst = np.sum((y-y_mean)**2)
        n =len(x)
        y_fit = np.zeros()
        for i in range(n):
            y_fit = f.Eval(x[i])
        sss = np.sum((y-y_fit)**2)
        return sss/sst

