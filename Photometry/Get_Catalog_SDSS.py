import sqlcl
import numpy
import libastro as LA
import sys
import os

CURRENT_DIR = os.path.dirname(__file__)
file_path_para = os.path.join(CURRENT_DIR, "Photometry.param")
parameter = numpy.genfromtxt(file_path_para, unpack = True, dtype = None)
keys,values  = parameter[0], parameter[1]

objname = str(values[0])
RA =  float(values[1])
DEC = float(values[2])
Filter = str(values[3])

Area = str(sys.argv[1])
Num = str(sys.argv[2])
lowlim = float(sys.argv[3])
highlim = float(sys.argv[4])

fullcat_name_path =  os.path.join(CURRENT_DIR,"Full_SDSS.dat")
trimmedcat_name_path = os.path.join(CURRENT_DIR,"Trimmed_SDSS.dat")
fullcat = open(fullcat_name_path,'w')
trimmedcat =open(trimmedcat_name_path,'w')

query = """
SELECT TOP """+str(Num)+"""
cast(str(p.ra,13,8) as float) as ra,cast(str(p.[dec],13,8) as float) as dec,p.psfMag_u,p.psfMag_g,p.psfMag_r,p.psfMag_i,p.psfMag_z,p.psfMagErr_u,p.psfMagErr_g,p.psfMagErr_r,p.psfMagErr_i,p.psfMagErr_z,dbo.fIAUFromEq(p.ra,p.[dec]) as SDSSname 
FROM ..PhotoObj AS p
"""+"JOIN dbo.fGetNearbyObjEq("+str(RA)+","+str(DEC)+","+str(Area)+") AS b ON b.objID = P.objID"

data = sqlcl.query(query).read()
#print data
print>>fullcat,str(data)
fullcat.close()
############################### slim down #########################

table = numpy.genfromtxt(fullcat_name_path,delimiter =',',dtype = str,skip_header = 2,unpack = True)
RA_star,DEC_star,psfMag_u,psfMag_g,psfMag_r,psfMag_i,psfMag_z,psfMagErr_u,psfMagErr_g,psfMagErr_r,psfMagErr_i,psfMagErr_z,SDSSname  = table[:]

RA_star = numpy.array(RA_star,dtype = float)
DEC_star= numpy.array(DEC_star,dtype = float)
psfMag_u= numpy.array(psfMag_u,dtype = float)
psfMag_g= numpy.array(psfMag_g,dtype = float)
psfMag_r= numpy.array(psfMag_r,dtype = float)
psfMag_i= numpy.array(psfMag_i,dtype = float)
psfMag_z= numpy.array(psfMag_z,dtype = float)
psfMagErr_u= numpy.array(psfMagErr_u,dtype = float)
psfMagErr_g= numpy.array(psfMagErr_g,dtype = float)
psfMagErr_r= numpy.array(psfMagErr_r,dtype = float)
psfMagErr_i= numpy.array(psfMagErr_i,dtype = float)
psfMagErr_z= numpy.array(psfMagErr_z,dtype = float)

### Mag conversion from Lupton 2005
Bmag = psfMag_g - 0.3130*(psfMag_g -psfMag_r) + 0.2271  
e_Bmag = (0.0107**2+ psfMagErr_g**2 + psfMagErr_r**2)**0.5

Rmag = psfMag_r - 0.2936*(psfMag_g -psfMag_r)-0.0971
e_Rmag = (0.0106**2+psfMagErr_g**2 + psfMagErr_r**2)**0.5

Vmag = psfMag_g - 0.5784*(psfMag_g -psfMag_r) + 0.0038
e_Vmag = (0.0054**2 + psfMagErr_g**2 + psfMagErr_r**2)**0.5

if Filter == 'B':
    print "B filter"
    Magcat,Magcaterr =Bmag , e_Bmag
    
if Filter == 'R':
    print "R filter"
    Magcat,Magcaterr =Rmag , e_Rmag
    
if Filter == 'V':
    print "V filter"
    Magcat,Magcaterr =Vmag , e_Vmag

if Filter == 'OIII':
    print "NB filter"
    Magcat,Magcaterr =Bmag , e_Bmag

for i in range(0,len(Magcat)):
    dist_qso = LA.distance(RA_star[i],DEC_star[i],float(RA),float(DEC))
    if  dist_qso > 3 and lowlim < float(Magcat[i]) < highlim and float(Magcat[i]) != 99.999 :
        #print dist_qso
        print>>trimmedcat, str(SDSSname[i].split(" ")[1])+'\t'+str(RA_star[i])+'\t'+str(DEC_star[i])+'\t'+str(Bmag[i])+'\t'+str(Rmag[i])+'\t'+str(Vmag[i])+'\t'+str(e_Bmag[i])+'\t'+str(e_Rmag[i])+'\t'+str(e_Vmag[i])
trimmedcat.close()
