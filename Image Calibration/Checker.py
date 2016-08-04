import numpy
import glob
import pyfits
import os

CURRENT_DIR = os.path.dirname(__file__) #get path
Filters = ["B","V","R","OIII","I"]

file_path_Bad = os.path.join(CURRENT_DIR, "BadWCS")
file_path_others = os.path.join(CURRENT_DIR, "others")

os.system("mkdir "+file_path_Bad)
os.system("mkdir "+file_path_others)

file_path_glob = os.path.join(CURRENT_DIR,"*.fits" )
Images = glob.glob(file_path_glob)
Images.sort()

for i in range(0,len(Images)):
    openIM = pyfits.open(Images[i])
    header = openIM[0].header 
    checklist = header.keys()
    if 'CD1_1' and 'CD1_2' not in  checklist:
        print Images[i] , "BAD WCS"
        os.system("mv "+str(Images[i])+" "+file_path_Bad)
    else:
        print Images[i] , "GOOD WCS"
    
for i in range(0,len(Filters)):
    filt = str(Filters[i])+"Band"
    path = os.path.join(CURRENT_DIR,filt)
    im = os.path.join(CURRENT_DIR,"*_"+str(Filters[i])+"_*")
    os.system("mkdir "+path)
    os.system("mv "+im+"  "+path)

os.system("mv *.fits "+file_path_others)

