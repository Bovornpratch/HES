# python Astro libary by Bovornpratch Vijarnwannaluk written on December 16th 2015 Current version is version 2"

print "loading Astrolib Ver.2  by Klod"

import numpy
import matplotlib.pyplot as plt
import matplotlib
import os
import glob
import pyfits

CURRENT_DIR = os.path.dirname(__file__)

def HEnamefinder(template,key):
    if type(template) is not str or  type(key) is not str:
        return "Wrong input type, input strings"
    else:
        pos = template.find(key)
        nametemp = template[pos:pos+12]
        #print nametemp[6]
        if nametemp[6] and nametemp[7]  == '-':
            print "Northern Dec"
            Name_set = template[pos:pos+6]+"+"+template[pos+8:pos+12]
        else:
            print "Southern Dec"
            Name_set = template[pos:pos+11]
        Name = str(Name_set)
        return Name


def RAcal(RaObj,key):
    if type(RaObj) is not str or  type(key) is not str:
        return "Wrong input ,pls enter strings"
    else:
        RaH = float(RaObj.split(key)[0])
        RaM = float(RaObj.split(key)[1])
        RaS = float(RaObj.split(key)[2])
        return (RaH+(RaM/60)+(RaS/3600))*15


def DECcal(DecObj,key):
    if type(DecObj) is not str or  type(key) is not str:
        return "Wrong input ,pls enter strings"
    else:
        DecD  = float(DecObj.split(key)[0])
        DecAM = float(DecObj.split(key)[1])
        DecAS = float(DecObj.split(key)[2])
        DecD_temp = DecObj.split(":")[0]
        print DecD , DecAM , DecAS
        if DecD_temp[0] == '+':
            print DecD + (DecAM/60.) + (DecAS/3600.)
            return  DecD + (DecAM/60.) + (DecAS/3600.)
        elif DecD_temp[0] == '-':
            return  DecD - (DecAM/60.) - (DecAS/3600.)


def mindist(Ra1 ,Dec1 ,Ra2 , Dec2):
    return numpy.amin( (((Ra1-Ra2)**2 + (Dec1-Dec2)**2)**0.5)*3600)

def distance(Ra1 ,Dec1 ,Ra2 , Dec2):
    return  ((((Ra1-Ra2)**2 + (Dec1-Dec2)**2)**0.5)*3600)

    
def posmin(Ra1 ,Dec1 ,Ra2 , Dec2):
    distmin = mindist(Ra1 ,Dec1 ,Ra2 , Dec2)
    array = (((Ra1-Ra2)**2 + (Dec1-Dec2)**2)**0.5)*3600
    return numpy.where(array == distmin)


def ZPval(mag,flux):
    return mag + 2.5*numpy.log10(flux)


def ZPERRval(magerr,flux,fluxerr):
    temp = (2.5*fluxerr)/(flux* numpy.log(10))
    return (magerr**2 + temp **2)**0.5


def MAGval(ZP,flux):
    return ZP - 2.5*numpy.log10(flux)


def MAGERRval(ZPERR , flux ,fluxerr):
    temp = (2.5*fluxerr)/(flux*numpy.log(10))
    return (ZPERR**2 + temp**2)**0.5


def Mag(flux):
    return -2.5*numpy.log10(flux)


def CleanUp():
    #rmS = os.path.join(CURRENT_DIR,"*_S.fits")
    #rmSS = os.path.join(CURRENT_DIR,"*_SS.fits")
    #os.system("rm "+rmS)
    #os.system("rm "+rmSS)

    os.system("rm *_SS.fits")
    os.system("rm *_S.fits")

    return 

def GetFits(Keys):
    Keys = str(Keys)
    file_path_fits = os.path.join(CURRENT_DIR,Keys)
    start = glob.glob(file_path_fits+"*.fits")
    start.sort()
    return start

def FirstFile(filelist):
    return filelist[0]

def Getcatalog(File,key):
    temp = pyfits.open(str(File))
    catalog = temp[1].data
    return catalog[str(key)]

def GetHECatalogIndex(Array,key):
    for i in range(0,len(Array)):
        tail = Array[i].split('HE')[1]
        x = "HE"+ tail[1:]
        if x == key :
            mark = i
        else:
            continue
    return mark

def GetFilter(Name,*filters):
    for i in range(0,len(filters)):
        if "_"+str(filters[i])+"_" in Name:
            flag = str(filters[i])
            print "Taken in "+str(filters[i])
        else:
            continue
    return flag
    
def GetHeaderData(Ref,key):
    temp = pyfits.open(str(Ref))
    catalog = temp[0].header
    return str(catalog[key])

def ObtainMJDs(Filelist):
    JDS = []
    for i in range(0,len(Filelist)):
        JD_temp = GetHeaderData(Filelist[i],'JD')
        JDS.append(float(JD_temp)-  2400000.5)
    return JDS

def GetPath():
    path = os.getcwd()
    new  = path.split('fits')[0]
    new  = new[:len(new)-1]
    return new

def NameGenerator(Obj,job,MJD,flag):
    Name = str(Obj)+"_"+str(job)+"_"+str(MJD)+"_"+str(flag)+"_S.fits"
    return Name

def Rename(Original, newname):
    os.system("mv "+Original+" "+newname)
    
def linecount(filename):
    text = open(str(filename),'r')
    txtlines = text.readlines()
    count = 0
    for i in range(0,len(txtlines)):
        count += 1
    return count

def GetColumnNames(text):
    x = open(text,'r')
    y = x.readlines()
    header = y[0]
    header = header[1:]
    header = header.split('\n')[0]
    columns = header.split('\t')
    return columns
        
def CheckAGN(Ra1,dec1,Ra2,dec2,lim):
    AGNDist = mindist(Ra1,dec1,Ra2,dec2)
    if AGNDist < lim:
        return "Y"
    else:
        return "N"
        
def CheckSTAR(Ra1,dec1,Ra2,dec2,lim):
    StarDist = mindist(Ra1,dec1,Ra2,dec2)
    if StarDist < lim:
        val = "Y"
    else:
        val = "N"
    return val


def CheckSN(flux, fluxerr, lim):
    SN = flux/fluxerr
    if SN > lim:
        flag =  "Y"
    else:
        flag = "N"
    return flag

def QCfunc(func, *functuple):
    if func == "N":
            flag = "N"
    else:
        if "N" in functuple:
            flag = "N"
        else:
            flag = "Y"
    return flag


def GetHES_Coor( Name ):
    temp = pyfits.open('hes_sample_monitoring.fits')
    catalog = temp[1].data 
    hename = catalog['hename']
    ra2000 = catalog['ra2000']
    dec2000 = catalog['dec2000']
    z = catalog['z']
    bj_spc = catalog['bj_spc']
    bj_cor = catalog['bj_cor']
    logM=catalog['Miz2']
    logL_bol=catalog['logLboli']
    
    ID = Name.split("HE")[1]
    print ID
    for i in range(0,len(hename)):
        if ID in hename[i]:
            print "Object "+str(hename[i])
            print "coordinate "+str(ra2000[i])+" "+str(dec2000[i])
            ra , dec = ra2000[i] , dec2000[i]
    return [float(ra),float(dec)]

def GetGoodList(Files):
    Good, Bad = 0,0
    Names = GetColumnNames(Files)
    #print Names
    txt = numpy.genfromtxt(str(Files),dtype=None ,names=Names ,unpack=True)
    SWARP_temp,EXTRACT_temp,MJD_temp,SCORE_temp = txt[Names[0]],txt[Names[1]],txt[Names[2]],txt[Names[3]]
    SWARP,EXTRACT,MJD,SCORE = [],[],[],[] 
    for i in range(0,len(SWARP_temp)):
        if SCORE_temp[i] == "Y":
            SWARP.append(SWARP_temp[i])
            EXTRACT.append(EXTRACT_temp[i])
            MJD.append(MJD_temp[i])
            SCORE.append(SCORE_temp[i])
            Good +=1
        else:
            Bad +=1
    print "Total Good"+'\t'+str(Good)+"/"+str(len(SWARP_temp))     
    print "Total Bad"+'\t'+str(Bad)+"/"+str(len(SWARP_temp))     
    array = numpy.vstack((SWARP,EXTRACT,MJD,SCORE))
    return array

def DataReductionParameter(Para):
    Parameters = numpy.genfromtxt(str(Para),dtype = None, unpack = True)
    return Parameters[1]

def Plot(File,ban,errorlim):
    MJD,ZP,ZPERR,FLUX,FLUXERR,MAG,MAGERR = [],[],[],[],[],[],[]
    data = numpy.loadtxt(File, unpack = True, dtype = float)
    MJD_TEMP,ZP_TEMP,ZPEER_TEMP,FLUX_TEMP,FLUXERR_TEMP,MAG_TEMP,MAGERR_TEMP = data[:]
    for j in range(0,len(MJD_TEMP)):
        if MAGERR_TEMP[j] < errorlim  :
            if MJD_TEMP[j] not in ban:
                
                MJD.append(MJD_TEMP[j])
                ZP.append(ZP_TEMP[j])
                ZPERR.append(ZPEER_TEMP[j])
                FLUX.append(FLUX_TEMP[j])
                FLUXERR.append(FLUXERR_TEMP[j])
                MAG.append(MAG_TEMP[j])
                MAGERR.append(MAGERR_TEMP[j]) 
            else:
                continue
        else:
            continue
    return [MJD,ZP,ZPERR,FLUX,FLUXERR,MAG,MAGERR]

def PlotPrint(Files,ban,errorlim):
    MJD,ZP,ZPERR,FLUX,FLUXERR,MAG,MAGERR = [],[],[],[],[],[],[]
    for i in range(0,len(Files)):
        data = numpy.loadtxt(Files[i], unpack = True, dtype = float)
        MJD_TEMP,ZP_TEMP,ZPEER_TEMP,FLUX_TEMP,FLUXERR_TEMP,MAG_TEMP,MAGERR_TEMP = data[:]
        for j in range(0,len(MJD_TEMP)):
            if MAGERR_TEMP[j] < errorlim  :
                if MJD_TEMP[j] not in ban:
                
                    MJD.append(MJD_TEMP[j])
                    ZP.append(ZP_TEMP[j])
                    ZPERR.append(ZPEER_TEMP[j])
                    FLUX.append(FLUX_TEMP[j])
                    FLUXERR.append(FLUXERR_TEMP[j])
                    MAG.append(MAG_TEMP[j])
                    MAGERR.append(MAGERR_TEMP[j]) 
                else:
                    continue
            else:
                continue

    return [MJD,ZP,ZPERR,FLUX,FLUXERR,MAG,MAGERR]
