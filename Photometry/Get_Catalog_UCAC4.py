from astroquery.vizier import Vizier
import astropy.units as u
import astropy.coordinates as coord
import numpy
import os
import sys

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


Vizier.ROW_LIMIT = Num
Search = Vizier(columns=["+_r",'UCAC4','_RAJ2000', '_DEJ2000','Bmag','Vmag','gmag','rmag','imag','e_Bmag','e_Vmag','e_gmag','e_rmag','e_imag'])

result = Search.query_region(coord.SkyCoord(RA,DEC,unit=(u.deg, u.deg),frame='icrs'),width=str(Area)+"m", catalog=["UCAC4"])
Catalog = result['I/322A/out']
print Catalog
Catalog.write('table.dat', format='ascii')

CURRENT_DIR = os.path.dirname(__file__)
fullcat_name_path =  os.path.join(CURRENT_DIR,"Full_UCAC4.dat")
fullcat = open(fullcat_name_path,'w')
Catalog.write(fullcat_name_path, format='ascii')

trimmedcat_name_path = os.path.join(CURRENT_DIR,"Trimmed_UCAC4.dat")
trimmedcat =open(trimmedcat_name_path,'w')


data = numpy.genfromtxt(fullcat_name_path, dtype = str, unpack = True,skip_header = 1)
rad,UCAC4,RAJ2000,DEJ2000,Bmag,Vmag,gmag,rmag,imag,e_Bmag,e_Vmag,e_gmag,e_rmag,e_imag = data[:]

if Filter == 'B':
    print "B filter"
    Magcat,Magcaterr =Bmag , e_Bmag
    
if Filter == 'R':
    print "R filter"
    Magcat,Magcaterr =rmag , e_rmag
    
if Filter == 'V':
    print "V filter"
    Magcat,Magcaterr =Vmag , e_Vmag

if Filter == 'OIII':
    print "NB filter"
    Magcat,Magcaterr =Bmag , e_Bmag

Name = []
RA_Star ,DEC_Star = [],[]
B_mag, R_mag, V_mag = [],[],[]
eB_mag, eR_mag, eV_mag = [],[],[]

for i in range(0,len(UCAC4)):
    #print UCAC4[i] , Magcat[i]
    if  str(Magcat[i]) != "--":
        if lowlim < float(Magcat[i]) < highlim:
            print UCAC4[i]
            if str(Bmag[i]) == "--":
                Bmag_p, e_Bmag_p = 99.99, 99.99
            else:
                Bmag_p, e_Bmag_p = Bmag[i] ,float(e_Bmag[i])*(10**-2)
                
            if str(rmag[i]) == "--":
                rmag_p, e_rmag_p = 99.99, 99.99
            else:
                rmag_p, e_rmag_p = rmag[i] ,float(e_rmag[i])*(10**-2)
            
            if str(Vmag[i]) == "--":
                Vmag_p, e_Vmag_p = 99.99, 99.99
            else:
                Vmag_p, e_Vmag_p =  Vmag[i] ,float(e_Vmag[i])*(10**-2)
                
            #print Bmag_p, e_Bmag_p
            #print rmag_p, e_rmag_p
            #print Vmag_p, e_Vmag_p

            
            print>>trimmedcat,str(UCAC4[i])+'\t'+str(RAJ2000[i])+'\t'+str(DEJ2000[i])+'\t'+str(Bmag_p)+'\t'+str(rmag_p)+'\t'+str(Vmag_p)+'\t'+str(e_Bmag_p)+'\t'+str(e_rmag_p)+'\t'+str(e_Vmag_p)
            
            
            




    




