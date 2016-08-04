import os
import sys
import numpy
import pyfits
import libastro  as LA
import glob

CURRENT_DIR = os.path.dirname(__file__)


Name = str(sys.argv[1])
Band = str(sys.argv[2])

file_path_param = os.path.join(CURRENT_DIR, 'Photometry.param')
txt = open(file_path_param,'w')

temp = Name.split('HE')[1]
AGNName = "HE "+temp

catpath = os.path.join(CURRENT_DIR,"hes_sample_monitoring.fits")
cat = pyfits.open(catpath)
cat_dat = cat[1].data
cat_head = cat[1].columns
titles =  cat_head.names
#print cat_dat[titles[0]]
pos =numpy.where(AGNName == cat_dat[titles[0]])
#print str(cat_dat[titles[0]][pos][0])
RA =  float(cat_dat[titles[1]][pos])
DEC =  float(cat_dat[titles[2]][pos])

print str(AGNName)
print str(RA),str(DEC)
print str(Band)

print >>txt,"Name"+'\t'+str(Name)
print >>txt,"RA"+'\t'+str(RA)
print >>txt,"DEC"+'\t'+str(DEC)
print >>txt,"FILTER_BAND"+'\t'+str(Band)
