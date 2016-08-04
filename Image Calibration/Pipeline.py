#!/usr/bin/python

import os
import sys
import glob

CURRENT_DIR = os.path.dirname(__file__)
file_path_Head = os.path.join(CURRENT_DIR, 'Header_read.py')
file_path_SWARP = os.path.join(CURRENT_DIR, 'ImStack.py')
file_path_SEX = os.path.join(CURRENT_DIR, 'Object_Extractor.py')
file_path_SCORE = os.path.join(CURRENT_DIR, 'HES_QC_script.py')



## parameters ##
Name = str(sys.argv[1])
binsize = 1

##function list##

os.system("python "+file_path_Head+" "+str(Name))
os.system("python "+file_path_SWARP+" "+str(binsize))
os.system("python "+file_path_SEX)
os.system("python "+file_path_SCORE)
