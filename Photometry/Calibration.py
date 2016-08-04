import numpy
import os
import matplotlib.pyplot as plt
import sys
import libastro as LA
import glob
import pylab
from matplotlib.backends.backend_pdf import PdfPages

CURRENT_DIR = os.path.dirname(__file__)
#file_path_cat = os.path.join(CURRENT_DIR,"Trimmed_SDSS.dat" )

#Files
File = str(sys.argv[1])
Catalog = str(sys.argv[2])
#Cut numbers
ELLIP = float(sys.argv[3])
FWHM_MAX = float(sys.argv[4])
SigClipLim = float(sys.argv[5])
factor = float(sys.argv[6])
print File

stars = numpy.genfromtxt(Catalog,dtype = str,unpack = True)
Name,RAstar,DECstar,Bmag,Rmag,Vmag,e_Bmag,e_Rmag,e_Vmag = stars[:]
RAstar = numpy.array(RAstar,dtype = float)
DECstar = numpy.array(DECstar,dtype = float)
Bmag = numpy.array(Bmag,dtype = float)
Rmag = numpy.array(Rmag,dtype = float)
Vmag = numpy.array(Vmag,dtype = float)
e_Bmag = numpy.array(e_Bmag,dtype = float)
e_Rmag = numpy.array(e_Rmag,dtype = float)
e_Vmag = numpy.array(e_Vmag,dtype = float)


Array = LA.GetGoodList(File)
SWARP,EXTRACT,MJD,SCORE = Array[:]
file_path_param = os.path.join(CURRENT_DIR,"Photometry.param")
parameter = numpy.genfromtxt(file_path_param, unpack = True, dtype = None)
keys,values  = parameter[0], parameter[1]
objname = str(values[0])
RA_AGN_REF =  float(values[1])
DEC_AGN_REF = float(values[2])
Filter = str(values[3])

if Filter == 'B':
    print "B filter"
    Magcat,Magcaterr =Bmag , e_Bmag
    
if Filter == 'R':
    print "R filter"
    Magcat,Magcaterr =Rmag , e_Rmag
    
if Filter == 'V':
    print "V filter"
    Magcat,Magcaterr =Vmag , e_Vmag
    
outname = (File.split("QC")[0]).split("Input_")[1]

file_path_star = os.path.join(CURRENT_DIR,outname+"StarsCheck.txt")
StarsCheck = open(file_path_star,'w')
file_path_diagg = os.path.join(CURRENT_DIR,outname+"SDSS_Diagnostics.pdf")
Diag =PdfPages(file_path_diagg)
file_path_data = os.path.join(CURRENT_DIR,outname+"Data_SDSS.dat")
Data = open(file_path_data,'w')
print>>Data, "#EXTRACT"+'\t'+"MJD"+'\t'+"ZP"+'\t'+"ZPERR"+'\t'+"FLUXAGN"+'\t'+"FLUXERR"+'\t'+"MagAGN"+'\t'+"MagerrAGN"

#-------------------------------------------------------------------------------
#Start calculations

#filter bad stars/sigma clip
RAstar_array_fil, DECstar_array_fil = [], []
ZP_array_fil, ZPERR_array_fil = [], []
mag_array_fil = []

print>>StarsCheck,"Start Total "+str(len(Magcat))+" stars from SDSS"+'\n'+"Filter Stars in all Epochs"

sigRaw = numpy.loadtxt(EXTRACT[0],skiprows=11,unpack=True)            
id_zp, Ra_zp, Dec_zp, mag_zp, MAGERR_BEST_zp, FLUX_BEST_zp, FLUXERR_BEST_zp, FWHM_WORLD_zp, ELLIPTICITY_zp, CLASS_STAR_zp,BACKGROUND_zp, Flux_max = sigRaw[:]
for i in range(0,len(Magcat)):
    min_dist = LA.mindist(Ra_zp,Dec_zp,RAstar[i],DECstar[i])
    pos_star= LA.posmin(Ra_zp,Dec_zp,RAstar[i],DECstar[i])
    if  ELLIPTICITY_zp[pos_star] < ELLIP and  FWHM_WORLD_zp[pos_star] < FWHM_MAX :
        ZP = LA.ZPval(Magcat[i], FLUX_BEST_zp[pos_star])
        ZPERR = LA.ZPERRval(0,FLUX_BEST_zp[pos_star],FLUXERR_BEST_zp[pos_star])
        mag_array_fil.append(Magcat[i])
        RAstar_array_fil.append(RAstar[i])
        DECstar_array_fil.append(DECstar[i])
        ZP_array_fil.append(ZP)
        ZPERR_array_fil.append(ZPERR)
        plt.scatter(1,ZP)
        
MEANZP,STDZP = numpy.median(ZP_array_fil),numpy.std(ZP_array_fil)
lim = SigClipLim
upperlim, lowerlim= MEANZP + lim*STDZP, MEANZP - lim*STDZP
print "filtered to",len(mag_array_fil)
print>>StarsCheck,"Total "+str(len(mag_array_fil))+" after Ellip/FWHM  Filter"
plt.errorbar(1,MEANZP,yerr=STDZP,fmt = 'o' ,color= 'r')
plt.title("unclipped ZP")
Diag.savefig()
#plt.show()
pylab.clf()

plt.hist(numpy.array(ZP_array_fil),30, normed= True)
plt.title("Unclipped ZP Histogram on "+str(MJD[0]))
plt.xlabel("ZP")
plt.ylabel("Normalized freq.")
Diag.savefig()
#plt.show()
plt.clf()

mag_array_sig, RAstar_array_sig, DECstar_array_sig, ZP_array_sig,ZPERR_array_sig   = [],[],[],[],[]
#SIGCLIP
for i in range(0,len(mag_array_fil)):
    #print RAstar_array_fil[i] , DECstar_array_fil[i] , ZP_array_fil[i] ,ZPERR_array_fil[i] 
    if lowerlim < ZP_array_fil[i] < upperlim:
        mag_array_sig.append(mag_array_fil[i])
        RAstar_array_sig.append(RAstar_array_fil[i])
        DECstar_array_sig.append(DECstar_array_fil[i])
        ZP_array_sig.append(ZP_array_fil[i])
        ZPERR_array_sig.append(ZPERR_array_fil[i])
        plt.scatter(1,ZP_array_fil[i])

print "Sigma clipped to"+str(len(mag_array_sig))
newmean,newstd = numpy.median(ZP_array_sig), numpy.std(ZP_array_sig)
print "Mean and SD is "+str(newmean)+"+_"+str(newstd)
print "After Clip (Epoch1): Total stars "+str(len(mag_array_sig))+" Med ZP ="+str(newmean)+"+-"+str(newstd)
print>>StarsCheck, "After Sigmaclip (Epoch1): Total stars"+str(len(mag_array_sig))+" Med ZP ="+str(newmean)+"+-"+str(newstd)

plt.errorbar(1,newmean,yerr = newstd,fmt = 'o' ,color= 'r')
plt.title("clipped ZP")
Diag.savefig()
#plt.show()
plt.clf()

plt.hist(numpy.array(ZP_array_sig),30, normed= True)
plt.title("clipped ZP Histogram on "+str(MJD[0]))
plt.xlabel("ZP")
plt.ylabel("Normalized freq.")
Diag.savefig()
#plt.show()
plt.clf()

############################ ZP CAL #######################################
ZP_Epoch,ZPERR_Epoch = [],[]
AGN_real,AGNERR_real = [], []

print>>StarsCheck,"ZP calculation and second sigmaclip"
print>>StarsCheck,"MJD"+'\t'+"Stars_before"+'\t'+"Stars_After"+'\t'+"ZP_Before"+'\t'+"ZPerr_Before"+"ZP_After"+'\t'+"ZPerr_BAfter"

for i in range(0,len(EXTRACT)):
    print "--------"
    print EXTRACT[i]
    
    temp_before_clip =[]
    temp_after_clip = []
    magmag = []
    
    day = numpy.loadtxt(EXTRACT[i],skiprows = 11,  unpack = True ,dtype = float)
    id_zp, Ra_zp, Dec_zp, mag_zp, MAGERR_BEST_zp, FLUX_BEST_zp, FLUXERR_BEST_zp, FWHM_WORLD_zp, ELLIPTICITY_zp, CLASS_STAR_zp,BACKGROUND_zp, Flux_max = day[:]
    
    mindiststar = LA.mindist(Ra_zp, Dec_zp, RA_AGN_REF, DEC_AGN_REF)
    posAGN = LA.posmin(Ra_zp, Dec_zp, RA_AGN_REF, DEC_AGN_REF)
    
    for j in range(0, len(mag_array_sig)):
        #print ID_sig[j] , RAstar_array_sig[j] , DECstar_array_sig[j] , mag_array_sig[j]
        mindiststar = LA.mindist(Ra_zp, Dec_zp,RAstar_array_sig[j], DECstar_array_sig[j])
        posstar = LA.posmin(Ra_zp, Dec_zp, RAstar_array_sig[j], DECstar_array_sig[j])
        ZPstar = LA.ZPval(mag_array_sig[j], FLUX_BEST_zp[posstar])
        temp_before_clip.append(ZPstar)
        magmag.append(mag_array_sig[j])
        
    #Clip2 using percentile 50
    numbefore = len(temp_before_clip) 
    refmed, stdzp  = numpy.median(temp_before_clip), numpy.std(temp_before_clip)
    
    limPup = factor*(numpy.percentile(temp_before_clip,80) - refmed)
    limPlow = factor*(refmed - numpy.percentile(temp_before_clip,20)) 
    uplim, lowlim  = refmed+limPup, refmed-limPlow
    
    magmagafter = []
    
    #print "Before clip: "+str(len(temp_before_clip))+" stars "+str(refmed)+'\t'+str(stdzp)+'\t'+str(numpy.mean(temp_before_clip))
    print "Before clip: "+"MJD"+str(MJD[i])+'\t'+str(len(temp_before_clip))+" stars "+str(refmed)+'\t'+str(stdzp)
    counters  = 0
    for k in range(0,len(temp_before_clip)):
        if  lowlim  < float(temp_before_clip[k]) < uplim :
            temp_after_clip.append(temp_before_clip[k])
            magmagafter.append(magmag[k])
            counters +=1
        else:
            continue
        
    numafter = len(temp_after_clip)
    ZP, ZPERR = float(numpy.median(temp_after_clip)),float(numpy.std(temp_after_clip))
    
    #print ZP, ZPERR
    plt.clf()
    day = float(MJD[i])
    plt.scatter(magmagafter,temp_after_clip)
    plt.xlabel("Mag")
    plt.ylabel("ZP")
    plt.title("ZP-Mag in "+str(MJD[i]))
    #Diag.savefig()

    #ZP, ZPERR = numpy.median(temp_after_clip), 
    #print "Percentile 75 ",  numpy.percentile(temp_after_clip,75),numpy.percentile(temp_after_clip,75) - ZP
    #print "Percentile 25 ",      numpy.percentile(temp_after_clip,25),ZP - numpy.percentile(temp_after_clip,25)
    print "After clip:  "+"MJD"+str(MJD[i])+'\t'+str(numafter)+" stars "+str(ZP)+'\t'+str(ZPERR)#+'\t'+str(numpy.mean(temp_after_clip))
    
    print>>StarsCheck,str(numbefore)+'\t'+str(numafter)+'\t'+str(refmed)+'\t'+str(stdzp)+'\t'+str(ZP)+'\t'+str(ZPERR)

    uperr = numpy.percentile(temp_after_clip,75) - ZP
    lowerr= ZP - numpy.percentile(temp_after_clip,25)
    
    if uperr > lowerr:
        errorr = uperr
    else:
        errorr = lowerr
        
    plt.errorbar(numpy.median(magmagafter),ZP, yerr = errorr, fmt = 'o', color = 'r')
    Diag.savefig()
    ZP_Epoch.append(ZP)
    ZPERR_Epoch.append(errorr)

    AGN_real.append(float(LA.MAGval(ZP_Epoch[i], FLUX_BEST_zp[posAGN])))
    AGNERR_real.append(float(LA.MAGERRval(ZPERR_Epoch[i], FLUX_BEST_zp[posAGN], FLUXERR_BEST_zp[posAGN])))
    
    print >>Data,str(MJD[i])+'\t'+str(ZP_Epoch[i])+'\t'+str(ZPERR_Epoch[i])+'\t'+str(float(FLUX_BEST_zp[posAGN]))+'\t'+str(float(FLUXERR_BEST_zp[posAGN]))+'\t'+str(float(AGN_real[i]))+'\t'+str(float(AGNERR_real[i]))

    #print >>Data,str(EXTRACT[i])+'\t'+str(MJD[i])+'\t'+str(ZP_Epoch[i])+'\t'+str(ZPERR_Epoch[i])+'\t'+str(float(FLUX_BEST_zp[posAGN]))+'\t'+str(float(FLUXERR_BEST_zp[posAGN]))

    #print str(MJD[i])+'\t'+str(ZP_Epoch[i])+'\t'+str(ZPERR_Epoch[i])+'\t'+str(float(AGN_real[i]))+'\t'+str(float(AGNERR_real[i]))
    #print str(MJD[i])+'\t'+str(ZP_Epoch[i])+'\t'+str(ZPERR_Epoch[i])

plt.clf()

plt.errorbar(MJD,ZP_Epoch,yerr = ZPERR_Epoch,fmt = 'o',color = 'b')
plt.title("ZP vs. MJD")
plt.xlabel("MJD")
plt.ylabel("ZP")
Diag.savefig()
#plt.show()
plt.clf()
Diag.close()

plt.errorbar(MJD,AGN_real,yerr = AGNERR_real,fmt = 'o',color = 'r')
plt.title("Lightcurve of "+str(objname)+" "+str(Filter))
plt.xlabel("MJD")
plt.ylabel("Mag")
plt.savefig(os.path.join(CURRENT_DIR,str(outname)+".png"))
#plt.show()
plt.clf()

