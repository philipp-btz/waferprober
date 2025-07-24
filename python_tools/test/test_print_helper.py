import sys
sys.path.append('..')
from print_helper import bcolors
bc = bcolors()
bc.example()

print(bc.OK+"This is Green for OK!!"+bc.ENDC)
print(bc.ERROR+"This is Red for Error!!"+bc.ENDC)
