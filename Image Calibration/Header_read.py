import os
import sys
import numpy
import pyfits
import libastro  as LA
import glob

CURRENT_DIR = os.path.dirname(__file__) #get path
searchField = "*.fits"

oldfilepath = os.path.join(CURRENT_DIR,"Input*")
getold = glob.glob(oldfilepath)
print getold
for i in range(len(getold)):
    command1 = "rm "+str(getold[i])
    print command1
    os.system(command1)


Name = sys.argv[1]
file_path_glob = os.path.join(CURRENT_DIR, str(searchField))
imagebay = []
search = glob.glob(file_path_glob)
for i in range(0,len(search)):
    #print search[i]
    if "hes_sample_monitoring.fits" in str(search[i]) or "_S.fits" in str(search[i]):
        continue
    else:
        imagebay.append(str(search[i]))
        #print search[i]
        

#print search

#print search
file_path_ref = os.path.join(CURRENT_DIR,"Pipeline.param")
txt = open(file_path_ref,'w')

temp = Name.split('HE')[1]
AGNName = "HE "+temp
#print AGNName

file_path_cat = os.path.join(CURRENT_DIR,'hes_sample_monitoring.fits')
cat = pyfits.open(file_path_cat)
cat_dat = cat[1].data
cat_head = cat[1].columns
titles =  cat_head.names
#print cat_dat[titles[0]]
pos =numpy.where(AGNName == cat_dat[titles[0]])
#print str(cat_dat[titles[0]][pos][0])
RA =  float(cat_dat[titles[1]][pos])
DEC =  float(cat_dat[titles[2]][pos])

print search[0]
RefIm = pyfits.open(imagebay[0])
Header = RefIm[0].header
#print Header
Band = Header['FILTER']
ID = Header['OBSID']

print str(AGNName)
print str(RA),str(DEC)
print str(Band)
print str(ID)

print >>txt,"Name"+'\t'+str(Name)
print >>txt,"RA"+'\t'+str(RA)
print >>txt,"DEC"+'\t'+str(DEC)
print >>txt,"FILTER_BAND"+'\t'+str(Band)
print >>txt,"ObsID"+'\t'+str(ID)

txt.close()
