
#this is the python sript to run the shell-like script
# Tiancheng Zhong 2021.07.22

import os
import sys
sys.path.append("..")
from print_helper import bcolors 
bc=bcolors()
#from my_python_package.print_helper import my_symbol as my_sym 
from collections import OrderedDict
#os.system("./set_env.sh")

py="python3.9"
exe="plot_signal_RMS.py"
dir_in="/media/archive/Data/irradiation/test_in_lab/noise_spectrum/"
#print(bc.WARNING+"Reminder: Did you source the ROOT 6.22?"+bc.ENDC)
#print(bc.WARNING+"Reminder: Are you using Python >=3.9?"+bc.ENDC)
#os.system("python3.9 AR_BURG_estimation.py")

matrix_start=0
matrix_stop=7
ch_start=1
ch_stop =15

for ch in range(ch_start,ch_stop+1,1):
    #print(f'{bc.INFO}ch{ch}{bc.ENC}')
    print(f'ch{ch}')
    for matrix in range(matrix_start,matrix_stop+1,1):
        #print(f'{bc.INFO}Matrix{matrix}{bc.ENC}')
        print(f'Matrix{matrix}')
        file_out=f'matrix{matrix}/RMS_results'
        os.system(f'{py} {exe} {dir_in} {file_out} {ch} {matrix}')
        #python3.9 plot_signal_RMS.py /media/archive/Data/irradiation/test_in_lab/noise_spectrum/ matrix1/RMS_results
