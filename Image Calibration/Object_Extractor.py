#Object extraction script using sextractor by Bovornpratch Vijarnwannaluk written on 4 April 2016

import numpy
import sys
import glob
import os
import libastro as LA

print "----------------------------------"
print "Extracting Objects using Sextractor"
print "----------------------------------"

CURRENT_DIR = os.path.dirname(__file__)
file_path_clean = os.path.join(CURRENT_DIR,"*Extracted.txt" )
oldfile = glob.glob(file_path_clean)

for i in range(0,len(oldfile)):
    os.system("rm "+str(oldfile[i]))

file_path_input = os.path.join(CURRENT_DIR,"Input_*.txt" )
inputtxt = glob.glob(file_path_input)
LinesNumbers = LA.linecount(inputtxt[0])
textColumns = LA.GetColumnNames(inputtxt[0])
outtext = inputtxt[0].split('.txt')[0] + "_Extracted.txt"
file_path_out = os.path.join(CURRENT_DIR,outtext)
outputtxt = open(file_path_out,'w')
print>>outputtxt, "#ImageFile"+'\t'+"TextFile"+'\t'+"MJD"


print outtext
Rawfits = numpy.genfromtxt(str(inputtxt[0]),unpack =True,dtype = None ,names=textColumns)
files , MJD = Rawfits[textColumns[0]],Rawfits[textColumns[1]]

file_path_default = os.path.join(CURRENT_DIR,'default.sex')
file_path_out = os.path.join(CURRENT_DIR,"Objects.txt")

if files.size == 1:
    loops = 1
    pathfile = os.path.join(CURRENT_DIR,str(files))
    os.system("sex "+pathfile+" -c "+file_path_default)
    os.system("awk '!/EOD/' Objects.txt > tempobject && mv tempobject "+file_path_out)
    Newname = str(files).split("_S.fits")[0] + "_SS.txt"
    pathname = os.path.join(CURRENT_DIR,Newname)
    LA.Rename(file_path_out, pathname)
    #print "Extracted"+'\t'+str(Newname)+'\t'+str(MJD[i])
    print>>outputtxt, str(files)+'\t'+str(Newname)+'\t'+str(MJD)
    
else:
    loops = len(files)
    for i in range(0,len(files)):
        print str(files[i])+'\t'+str(MJD[i])
        #print str(files[i])+'\t'+str(MJD[i])
        pathfile = os.path.join(CURRENT_DIR,files[i])
        os.system("sex "+pathfile+" -c "+file_path_default)
        os.system("awk '!/EOD/' Objects.txt > tempobject && mv tempobject "+file_path_out)
        Newname = files[i].split("_S.fits")[0] + "_SS.txt"
        pathname = os.path.join(CURRENT_DIR,Newname)
        LA.Rename(file_path_out, pathname)
        #print "Extracted"+'\t'+str(Newname)+'\t'+str(MJD[i])
        print>>outputtxt, str(files[i])+'\t'+str(Newname)+'\t'+str(MJD[i])
    
outputtxt.close()

