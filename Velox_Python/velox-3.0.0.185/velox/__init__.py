
"""Determines the version of the sci module to import"""
from sys import version_info
from velox.vxmessageserver import *

if (version_info[0] > 2 and version_info[1] >= 5):
    from velox.sci35 import *
else:
    from velox.sci27 import *
