
from unittest import result
from uuid import NAMESPACE_X500
import numpy as np
from scipy.fft import fft, fftfreq
from scipy import signal
import ROOT



class mapping_helper:
    vec_UID_single=np.asarray([
        [3,7,11,15],
        [2,6,10,14],
        [1,5,9,13],
        [0,4,8,12]
    ]) #this is matrix4
    vec_scopeID_single=np.asarray([
        [13,10,9,2],
        [8,14,7,5],
        [12,15,0,3],
        [11,1,6,4]
    ]) #this is matrix4
    N_x = 8
    N_y = 12
    vec_sim_ch=np.full((N_x,N_y),-1,dtype=int)
    vec_UID_ch=np.full((N_x,N_y),-1,dtype=int)
    vec_scope_ch=np.full((N_x,N_y),-1,dtype=int)
    matrix_gap=20   # this should >=16
    line_gap=20     # 20 used in the irradiation testbeam simulation
    dict_UID_to_all={}
    def __init__(self):
        print("mapping_helper:: init...")
        self.init_test_mapping()
        self.init_sim_mapping()
        self.map_UID_to_all()
    
    def init_test_mapping(self):
        for matrixID in range(1,7):
            rotate=False
            if matrixID<4:
                rotate=True
            for x in range(4):
                for y in range(4):
                    a=x
                    b=y+(matrixID-4)*4
                    if rotate:
                        a = 3-x + 4
                        b = 3-y + (matrixID-1)*4
                    #print(f"{matrixID} (rotated: {rotate}): [{x,y}] UID={self.vec_UID_single[x][y]} ==> [{a,b}]")
                    self.vec_UID_ch[a][b] = self.vec_UID_single[x][y]+matrixID*self.matrix_gap
                    self.vec_scope_ch[a][b] = self.vec_scopeID_single[x][y]+matrixID*self.matrix_gap
    def init_sim_mapping(self):
        for x in range(self.N_x):
            for y in range(self.N_y):
                self.vec_sim_ch[x][y] = x + y*self.line_gap
    def get_UID_mappingHist2(self):
        h2d = ROOT.TH2I("UID_mapping","UID mapping",self.N_x,0.,float(self.N_x),self.N_y,0.,float(self.N_y))
        for x in range(len(self.vec_UID_ch)):
            for y in range(len(self.vec_UID_ch[0])):
                h2d.SetBinContent(x+1,y+1,self.vec_UID_ch[x][y])
        return h2d
    def get_UID_mappingHist2_local(self):
        h2d = ROOT.TH2I("UID_mapping_local","UID mapping local",self.N_x,0.,float(self.N_x),self.N_y,0.,float(self.N_y))
        for x in range(len(self.vec_UID_ch)):
            for y in range(len(self.vec_UID_ch[0])):
                h2d.SetBinContent(x+1,y+1,self.vec_UID_ch[x][y]%self.matrix_gap)
        return h2d

    def get_scope_mappingHist2(self):
        h2d = ROOT.TH2I("scope_mapping","scope mapping",self.N_x,0.,float(self.N_x),self.N_y,0.,float(self.N_y))
        for x in range(len(self.vec_scope_ch)):
            for y in range(len(self.vec_scope_ch[0])):
                h2d.SetBinContent(x+1,y+1,self.vec_scope_ch[x][y])
        return h2d
    def get_scope_mappingHist2_local(self):
        h2d = ROOT.TH2I("scope_mapping_local","scope mapping local",self.N_x,0.,float(self.N_x),self.N_y,0.,float(self.N_y))
        for x in range(len(self.vec_scope_ch)):
            for y in range(len(self.vec_scope_ch[0])):
                h2d.SetBinContent(x+1,y+1,self.vec_scope_ch[x][y]%self.matrix_gap)
        return h2d

    def get_sim_mappingHist2(self):
        h2d = ROOT.TH2I("sim_mapping","sim mapping",self.N_x,0.,float(self.N_x),self.N_y,0.,float(self.N_y))
        for x in range(len(self.vec_sim_ch)):
            for y in range(len(self.vec_sim_ch[0])):
                h2d.SetBinContent(x+1,y+1,self.vec_sim_ch[x][y])
        return h2d
    
    def get_position(self,ch,ID_sys):
        mapping=[]
        if ID_sys=="UID":
            mapping =  self.vec_UID_ch
        elif ID_sys == "sim":
            mapping =  self.vec_sim_ch
        elif ID_sys == "scope":
            mapping =  self.vec_scope_ch
        else:
            print(f"ID_sys={ID_sys} not found! potential option: [UID],[sim],[scope]")
            return -1,-1

        pos= np.where(mapping==ch)
        #print(f"{ID_sys}, {ch}=>{pos}; {mapping}")
        if len(pos[0])!=1:
            print(f"{len(pos[0])} different position found! something wrong!!")
        return pos[0][0],pos[1][0]

    def map_UID_to_all(self):
        for i_matrix in range(8):
            for i_ch in range(16):
                UID = i_matrix*20+i_ch
                x_local = int(np.where(self.vec_UID_single==i_ch)[0][0])
                y_local = int(np.where(self.vec_UID_single==i_ch)[1][0])
                scope_ID = i_matrix*20 + self.vec_scopeID_single[x_local][y_local]
                sim_ID = -1
                if i_matrix >0 and i_matrix<7:
                    x_global = int(np.where(self.vec_UID_ch==UID)[0][0])
                    y_global = int(np.where(self.vec_UID_ch==UID)[1][0])
                    sim_ID = self.vec_sim_ch[x_global][y_global]
                self.dict_UID_to_all[UID] = [scope_ID,sim_ID]
    def lookup_map(self,ID,type_from,type_to): #typefrom and to can be "UID", "scope_ID", "sim_ID" # return value: -1: not in simulation(good) -2: bad
        ID_return =-2
        if type_from=="UID" and (ID in self.dict_UID_to_all.keys()):
            if type_to=="scope_ID":
                ID_return = self.dict_UID_to_all[ID][0]
            elif type_to =="sim_ID":
                ID_return = self.dict_UID_to_all[ID][1]
        elif type_from=="scope_ID":
            ID_return = self.look_up_scope_ID_or_sim_ID(ID,True,type_to)
        elif type_from=="sim_ID":
            ID_return = self.look_up_scope_ID_or_sim_ID(ID,False,type_to)
        else:
            print("no type_from:{type_to}")
        return ID_return
    def look_up_scope_ID_or_sim_ID(self,ID,bool_from_scope_ID,type_to):
        ID_return =-2
        for UID in self.dict_UID_to_all.keys():
            if bool_from_scope_ID and self.dict_UID_to_all[UID][0]==ID:
                if type_to=="UID":
                    ID_return = UID
                elif type_to =="sim_ID":
                    ID_return = self.dict_UID_to_all[UID][1]
                else:
                    print(f"type_to:{type_to} is wrong")
            elif bool_from_scope_ID==False and self.dict_UID_to_all[UID][1]==ID:
                if type_to=="UID":
                    ID_return = UID
                elif type_to =="scope_ID":
                    ID_return =  self.dict_UID_to_all[UID][0]
                else:
                    print(f"type_to:{type_to} is wrong")
        return ID_return
