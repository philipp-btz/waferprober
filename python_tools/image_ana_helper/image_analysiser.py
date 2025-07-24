import numpy as np
import math 
import ROOT

class image_analysiser:
    k_b = 8.617333e-5       #boltzman constant
    C_to_K_Const=273.15     
    E_a=0
    def __init__(self):
        pass
    def test(self):
        print("this is a test")
    
    def get_gray_hist(self,img,scale=255): # get the gray_scale hist
        (h,w) = img.shape[:2]
        hist_gray =ROOT.TH1D("hist_gray","hist gray",scale,0,scale)
        for i_x in range(h):
            for i_y in range(w):
                hist_gray.Fill(img[i_x][i_y])
        return hist_gray

    def BG_remove(self,img_orig,img_bg):    #manually remove the BG
        (h,w) = img_orig.shape[:2]
        (h_bg,w_bg) = img_bg.shape[:2]
        if h!=h_bg or w!=w_bg:
            print("Error: size of original picture and BG picture is not the same")
            return img_orig
        for i_x in range(h):
            for i_y in range(w):
                sig = img_orig[i_x][i_y]
                bg  = img_bg[i_x][i_y]
                pure_sig = 0
                if sig>bg:
                    pure_sig = sig - bg
                img_orig[i_x][i_y] =pure_sig 
        return img_orig
        
    