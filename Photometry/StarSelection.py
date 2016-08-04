import numpy
import os
import sys
import libastro as LA
import glob

CURRENT_DIR = os.path.dirname(__file__)
file_path_cat = os.path.join(CURRENT_DIR,"Trimmed*" )
catpatname = glob.glob(file_path_cat)[0]

starlist = numpy.genfromtxt(catpatname,unpack = True , dtype = str)
Name,RAstar,DECstar,Bmag,Rmag,Vmag,e_Bmag,e_Rmag,e_Vmag = starlist[:]

RAstar = numpy.array(RAstar,dtype = float)
DECstar = numpy.array(DECstar,dtype = float)
Bmag = numpy.array(Bmag,dtype = float)
Rmag = numpy.array(Rmag,dtype = float)
Vmag = numpy.array(Vmag,dtype = float)
e_Bmag = numpy.array(e_Bmag,dtype = float)
e_Rmag = numpy.array(e_Rmag,dtype = float)
e_Vmag = numpy.array(e_Vmag,dtype = float)

Files =str(sys.argv[1])
#file_path_input = os.path.join(CURRENT_DIR,"Input_*_QC.txt")
#Files = glob.glob(file_path_input)
#Files.sort()
print Files
Array = LA.GetGoodList(Files)
SWARP,EXTRACT,MJD,SCORE = Array[:]
outname = os.path.join(CURRENT_DIR,"LiveStar.list")

txt = open(outname,'w')
print>>txt,"#Name"+'\t'+"RA"+'\t'+"DEC"+'\t'+"Bmag"+'\t'+"Rmag"+'\t'+"Vmag"+'\t'+"e_Bmag"

for i in range(0,len(Name)):
    RAtemp,DECtemp = RAstar[i],DECstar[i]
    temp_check = []
    #print Name[i]
    for j in range(0,len(EXTRACT)):
        #print EXTRACT[j]
        file_path_epoch = os.path.join(CURRENT_DIR,EXTRACT[j])
        epoch_dat = numpy.loadtxt(file_path_epoch,dtype = float ,unpack = True,skiprows = 11)
        id_zp, Ra_zp, Dec_zp, mag_zp, MAGERR_BEST_zp, FLUX_BEST_zp, FLUXERR_BEST_zp, FWHM_WORLD_zp, ELLIPTICITY_zp, CLASS_STAR_zp,BACKGROUND_zp, Flux_max = epoch_dat[:]
        dist = LA.mindist(Ra_zp,Dec_zp,RAstar[i],DECstar[i])
        pos = LA.posmin(Ra_zp,Dec_zp,RAstar[i],DECstar[i])
        flux = FLUX_BEST_zp[pos]
        if dist < 3:
            temp_check.append('Y')
            #print dist, flux
        else:
            temp_check.append('N')
    if 'N' in temp_check:
        continue
    else:
        print "Go "+str(Name[i])
        print >>txt,str(Name[i])+'\t'+str(RAstar[i])+'\t'+str(DECstar[i])+'\t'+str(Bmag[i])+'\t'+str(Rmag[i])+'\t'+str(Vmag[i])+'\t'+str(e_Bmag[i])+'\t'+str(e_Rmag[i])+'\t'+str(e_Vmag[i])

txt.close()
