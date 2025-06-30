import numpy as np
import ROOT

class root_helper:
    def __init__(self) -> None:
        pass
    
    def Draw_2_plt_ratio(self,gr,gr_base,canvas_name="canvas",legend1="gr",legend2="gr_base",LogY=False,LogX=False,GridY=True,GridX=True):
        canvas=ROOT.TCanvas(canvas_name)
        
        #pad 1
        canvas.cd()
        pad1 = ROOT.TPad("pad1","pad1",0,0.3,1,1)
        pad1.SetBottomMargin(0)
        pad1.SetLogy(LogY)
        pad1.SetLogx(LogX)
        pad1.Draw()
        pad1.cd()
        gr.SetTitle("")
        gr.GetXaxis().SetLabelSize(0)
        gr.GetXaxis().SetTitleSize(0)
        gr.GetYaxis().SetTitleSize (0.05)
        gr.Draw()
        
        #pad 2
        canvas.cd()
        pad2 = ROOT.TPad("pad2","pad2",0,0.05,1,0.3)
        pad2.SetTopMargin(0)
        pad2.SetBottomMargin(0.25)
        pad2.Draw()
        pad2.cd()
        gr_base.SetTitle("")
        gr_base.GetXaxis().SetLabelSize (0.12)
        gr_base.GetXaxis().SetTitleSize (0.12)
        gr_base.GetYaxis().SetLabelSize (0.1)
        gr_base.GetYaxis().SetTitleSize (0.15)
        #gr_base.GetYaxis().SetTitle (" Data /MC")
        gr_base.GetYaxis().SetTitleOffset (0.3)
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
        
        return canvas
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

    def cal_diff_gr_to_f_fit(self,gr,f_fit,bool_norm=True):
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
            print(y[i],y_fit,diff_curr)
            if bool_norm:
                diff_curr =  diff_curr/y_fit
                diffE_curr = diffE_curr/y_fit
            print(diff_curr)
            gr_diff.SetPoint(gr_diff.GetN(),x[i],diff_curr)
            #gr_diff.SetPointError(gr_diff.GetN()-1,x_Err[i],diffE_curr[i])
        return gr_diff
    
    def write_grs(self,grs,dir):
        dir.cd()
        for gr in grs:
            gr.Write()

    def get_gr_1st_derivative(self, gr):
        x = np.asarray(gr.GetX())
        y = np.asarray(gr.GetY())
        n_points = gr.GetN()
        if n_points < 2:
            print("Error: TGraph must have at least 2 points to calculate the derivative.")
            return None  # Handle the error case
        gr_tmp = ROOT.TGraph()
        for i in range(n_points-1):
            gr_tmp.SetPoint(gr_tmp.GetN(),(x[i]+x[i+1])/2.,(y[i+1]-y[i])/0.1) # changed the quotient for the y-value of the TGraph from (Delta y/2.) to (Delta y/Delta x)
        return gr_tmp
    
    def get_gr_nth_derivative(self, gr,n_order):
        gr_tmp  = gr
        for i_do_deri in range(n_order):
            gr_tmp = self.get_gr_1st_derivative(gr_tmp)
        return gr_tmp
    
    def merge_tgraph(self, Tgraph_from, TGraph_to,x_offset,bool_with_error=False):
        for i in range(Tgraph_from.GetN()):
            TGraph_to.SetPoint(TGraph_to.GetN(),x_offset+Tgraph_from.GetX()[i],Tgraph_from.GetY()[i])
            if bool_with_error and type(TGraph_to)==type(ROOT.TGraphErrors()) and type(Tgraph_from)==type(ROOT.TGraphErrors()):
                TGraph_to.SetPointError(TGraph_to.GetN()-1,Tgraph_from.GetEX()[i],Tgraph_from.GetEY()[i])
        return TGraph_to
    
    def inverse_logarithmic_derivative(self, gr):
        '''
        Calculates the inverse of the logarithmic derivative of a ROOT.TGraph,    excluding points where division by zero would occur.
        Args:
            gr (ROOT.TGraph): The input TGraph.

        Returns:
            ROOT.TGraph: A new TGraph containing the inverse logarithmic derivative,
                     excluding points where the denominator is zero.
                     
        '''
        gr_der = self.get_gr_1st_derivative(gr)
        dx = np.array(gr_der.GetX())
        dy = np.array(gr_der.GetY())
        y = np.array(gr.GetY())
        n = np.size(dx)
        gr_tmp = ROOT.TGraph()

        for i in range(n):
            if y[i] != 0:
                ratio = dy[i] / y[i]
                if ratio != 0:
                    gr_tmp.SetPoint(gr_tmp.GetN(), dx[i], 1 / ratio)
                else:
                    print(f"Warning: Skipping point at x={dx[i]} because dy[{i}]/y[{i}] is zero.")
            else:
                print(f"Warning: Skipping point at x={dx[i]} because y[{i}] is zero, leading to division by zero.")
        return gr_tmp