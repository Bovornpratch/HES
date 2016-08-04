# python quality checher by Bovornpratch Vijarnwannaluk written on June 21st 2015 Current version is version 3"

import numpy
import os
import sys
import glob
import libastro as LA

dist_lim = 1
SNlim = 12

CURRENT_DIR = os.path.dirname(__file__)

file_extract = os.path.join(CURRENT_DIR,"Input*_Extracted.txt")
filelist = glob.glob(file_extract)
print filelist

Catalogfile = filelist[0]
Output_temp = Catalogfile.split("_Extracted.txt")[0]

Output_txt = Output_temp+"_QC.txt"
file_out = os.path.join(CURRENT_DIR,Output_txt)
Outprint = open(file_out,'w')
print>>Outprint,"#"+"SWARP"+'\t'+"Extract"+'\t'+"MJD"+'\t'+"Score"

print Output_txt

LinesNumbers = LA.linecount(Catalogfile)
textColumns = LA.GetColumnNames(Catalogfile)
print textColumns
inputdata  = numpy.genfromtxt(Catalogfile,unpack =True,dtype = None,names=textColumns)
Fits, extracted, MJD = inputdata[textColumns[0]],inputdata[textColumns[1]],inputdata[textColumns[2]]

#Coordinate = LA.GetHES_Coor("HE0345+0056")
file_pip = os.path.join(CURRENT_DIR,"Pipeline.param")
parameter = numpy.genfromtxt(file_pip, unpack = True, dtype = None)
keys,values  = parameter[0], parameter[1]

RA_AGN = float(values[1])
DEC_AGN = float(values[2])

ObsQC = []

if MJD.size == 1:
    objdata = os.path.join(CURRENT_DIR,str(extracted))
    objects = numpy.loadtxt(objdata,unpack = True, dtype = float, skiprows = 11)
    ids, ra, dec, mag, MAGERR_BEST, FLUX_BEST, FLUXERR_BEST,FWHM_WORLD, ELLIPTICITY, CLASS_STAR, BACKGROUND, FLUX_MAX = objects[:] 
    distance = LA.mindist(ra,dec,RA_AGN,DEC_AGN)
    index = LA.posmin(ra,dec,RA_AGN,DEC_AGN)
    #print distance, index
    
    AGN_exist = LA.CheckAGN(ra[index],dec[index],RA_AGN,DEC_AGN,dist_lim)
    print "AGN existenc "+str(AGN_exist)
    
    SignalNoise = LA.CheckSN(FLUX_BEST[index],FLUXERR_BEST[index],SNlim)
    print "Signal to noise "+str(SignalNoise)
    
    Quality = LA.QCfunc(AGN_exist,SignalNoise)
    #print str(extracted[i])+'\t'+str(Quality)
    print "-----"
    ObsQC.append(Quality)

    for i in range(0,len(ObsQC)):
        pathoutFit = os.path.join(CURRENT_DIR,str(Fits))
        pathoutex = os.path.join(CURRENT_DIR,str(extracted))
        print>>Outprint, str(pathoutFit)+'\t'+str(pathoutex)+'\t'+str(MJD)+'\t'+str(ObsQC[0])
        print str(extracted)+'\t'+str(ObsQC)
    
else:

    for i in range(0,len(MJD)):
        print extracted[i]
        objdata = os.path.join(CURRENT_DIR,extracted[i])
        objects = numpy.loadtxt(objdata,unpack = True, dtype = float, skiprows = 11)
        ids, ra, dec, mag, MAGERR_BEST, FLUX_BEST, FLUXERR_BEST,FWHM_WORLD, ELLIPTICITY, CLASS_STAR, BACKGROUND, FLUX_MAX = objects[:] 
        distance = LA.mindist(ra,dec,RA_AGN,DEC_AGN)
        index = LA.posmin(ra,dec,RA_AGN,DEC_AGN)
        #print distance, index
        
        AGN_exist = LA.CheckAGN(ra[index],dec[index],RA_AGN,DEC_AGN,dist_lim)
        print "AGN existenc "+str(AGN_exist)
        
        SignalNoise = LA.CheckSN(FLUX_BEST[index],FLUXERR_BEST[index],SNlim)
        print "Signal to noise "+str(SignalNoise)
        
        Quality = LA.QCfunc(AGN_exist,SignalNoise)
        #print str(extracted[i])+'\t'+str(Quality)
        print "-----"
        ObsQC.append(Quality)

    
    for i in range(0,len(ObsQC)):
        pathoutFit = os.path.join(CURRENT_DIR,str(Fits[i]))
        pathoutex = os.path.join(CURRENT_DIR,str(extracted[i]))
        print>>Outprint, str(pathoutFit)+'\t'+str(pathoutex)+'\t'+str(MJD[i])+'\t'+str(ObsQC[i])
        print str(extracted[i])+'\t'+str(ObsQC[i])

Outprint.close()
