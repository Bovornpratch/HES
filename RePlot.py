import numpy
import os
import matplotlib.pyplot as plt
import sys
import glob
import pylab
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib
from matplotlib.ticker import ScalarFormatter

CURRENT_DIR = os.path.dirname(__file__)

outfile = PdfPages("HES_Calibrated.pdf")

pathguide = os.path.join(CURRENT_DIR,"Calibration_Guild.txt")
guide = numpy.genfromtxt(pathguide,dtype = str, unpack = True)
Obj,RA,DEC,CAT  = guide[:]

for i in range(0,len(Obj)):
    #print Obj[i]

    file_path_data = os.path.join(CURRENT_DIR,str(Obj[i])+"*Data_ph.dat")
    #file_path_data = os.path.join(CURRENT_DIR,str(Obj[i])+"*Data_SDSS.dat")

    datafiles = glob.glob(file_path_data)
    NumFiles = len(datafiles)
    if NumFiles == 0:
        #print "----------"

        continue
    else:
        MJD_bo,ZP_bo,ZPERR_bo,FLUXAGN_bo,FLUXERR_bo,MagAGN_bo,MagerrAGN_bo = [],[],[],[],[],[],[]
        MJD_ro,ZP_ro,ZPERR_ro,FLUXAGN_ro,FLUXERR_ro,MagAGN_ro,MagerrAGN_ro = [],[],[],[],[],[],[]
        MJD_vo,ZP_vo,ZPERR_vo,FLUXAGN_vo,FLUXERR_vo,MagAGN_vo,MagerrAGN_vo = [],[],[],[],[],[],[]
        
        emp_b,emp_r,emp_v = 0,0,0
        fil_b,fil_r,fil_v = 0,0,0
        print str(Obj[i])+" has "+str(NumFiles)+" Files"

        for j in range(0,NumFiles):
            if '_B_' in datafiles[j]:
                #print datafiles[j]
                test = open(str(datafiles[j]),'r')
                if len(test.readlines()) == 1:
                    #print str(datafiles[j])+" Empty File"
                    emp_b += 1
                    continue
                else:
                    #print str(datafiles[j])+" Filled File"
                    bload = numpy.loadtxt(str(datafiles[j]), dtype = float , unpack = True)
                    MJD_b,ZP_b,ZPERR_b,FLUXAGN_b,FLUXERR_b,MagAGN_b,MagerrAGN_b = bload[:]
                    
                    plt.errorbar(MJD_b,MagAGN_b,yerr =MagerrAGN_b , color = 'b', fmt = 'o' )
                    ax = plt.gca()
                    ax.get_xaxis().get_major_formatter().set_useOffset(False)
                    ax.get_yaxis().get_major_formatter().set_useOffset(False)

                    plt.xlabel("MJD")
                    plt.ylabel("Mag")
                    plt.title(str(Obj[i])+" B "+str(CAT[i]))
                    fil_b +=1
                    
                    MJD_bo = numpy.append(MJD_bo,MJD_b)
                    ZP_bo= numpy.append(ZP_bo,ZP_b)
                    ZPERR_bo= numpy.append(ZPERR_bo,ZPERR_b)
                    FLUXAGN_bo= numpy.append(FLUXAGN_bo,FLUXAGN_b)
                    FLUXERR_bo= numpy.append(FLUXERR_bo,FLUXERR_b)
                    MagAGN_bo= numpy.append(MagAGN_bo,MagAGN_b)
                    MagerrAGN_bo= numpy.append(MagerrAGN_bo,MagerrAGN_b)
                    
            else:
                continue
        if str(fil_b) != '0':
            outfile.savefig()
            plt.clf()
        else:
            plt.clf()
        
         

        for j in range(0,NumFiles):
            if '_R_' in datafiles[j]:
                #print datafiles[j]
                test = open(str(datafiles[j]),'r')
                if len(test.readlines()) == 1:
                    #print str(datafiles[j])+" Empty File"
                    emp_r +=1
                    continue
                else:
                    rload = numpy.loadtxt(str(datafiles[j]), dtype = float , unpack = True)
                    MJD_r,ZP_r,ZPERR_r,FLUXAGN_r,FLUXERR_r,MagAGN_r,MagerrAGN_r = rload[:]                    
                    
                    plt.errorbar(MJD_r,MagAGN_r,yerr =MagerrAGN_r , color = 'r', fmt = 'o' )
                    ax = plt.gca()
                    ax.get_xaxis().get_major_formatter().set_useOffset(False)
                    ax.get_yaxis().get_major_formatter().set_useOffset(False)

                    plt.xlabel("MJD")
                    plt.ylabel("Mag")
                    plt.title(str(Obj[i])+" R "+str(CAT[i]))
                    fil_r +=1
                    #print str(datafiles[j])+" Filled File"
                    
                    MJD_ro = numpy.append(MJD_ro,MJD_r)
                    ZP_ro= numpy.append(ZP_ro,ZP_r)
                    ZPERR_ro= numpy.append(ZPERR_ro,ZPERR_r)
                    FLUXAGN_ro= numpy.append(FLUXAGN_ro,FLUXAGN_r)
                    FLUXERR_ro= numpy.append(FLUXERR_ro,FLUXERR_r)
                    MagAGN_ro= numpy.append(MagAGN_ro,MagAGN_r)
                    MagerrAGN_ro= numpy.append(MagerrAGN_ro,MagerrAGN_r)
                    
            else:
                continue

        if str(fil_r) != '0':
            outfile.savefig()
            plt.clf()
        else:
            plt.clf()


        for j in range(0,NumFiles):
            if '_V_' in datafiles[j]:
                #print datafiles[j]
                test = open(str(datafiles[j]),'r')
                if len(test.readlines()) == 1:
                    emp_v +=1
                    #print str(datafiles[j])+" Empty File"
                    continue
                else:
                    vload = numpy.loadtxt(str(datafiles[j]), dtype = float , unpack = True)
                    MJD_v,ZP_v,ZPERR_v,FLUXAGN_v,FLUXERR_v,MagAGN_v,MagerrAGN_v = vload[:]
                    
                    plt.errorbar(MJD_v,MagAGN_v,yerr =MagerrAGN_v , color = 'g', fmt = 'o' )
                    ax = plt.gca()
                    ax.get_xaxis().get_major_formatter().set_useOffset(False)
                    ax.get_yaxis().get_major_formatter().set_useOffset(False)

                    plt.xlabel("MJD")
                    plt.ylabel("Mag")
                    plt.title(str(Obj[i])+" V "+str(CAT[i]))
                    fil_v += 1
                    #print str(datafiles[j])+" Filled File"
                    
                    MJD_vo = numpy.append(MJD_vo,MJD_v)
                    ZP_vo= numpy.append(ZP_vo,ZP_v)
                    ZPERR_vo= numpy.append(ZPERR_vo,ZPERR_v)
                    FLUXAGN_vo= numpy.append(FLUXAGN_vo,FLUXAGN_v)
                    FLUXERR_vo= numpy.append(FLUXERR_vo,FLUXERR_v)
                    MagAGN_vo= numpy.append(MagAGN_vo,MagAGN_v)
                    MagerrAGN_vo= numpy.append(MagerrAGN_vo,MagerrAGN_v)
                    
            else:
                continue

        if str(fil_v) != '0':
            outfile.savefig()
            plt.clf()
        else:
            plt.clf()
        print "B "+str(emp_b)+" empty "+str(fil_b)+" filled, total lenght "+str(len(MJD_bo))
        print "R "+str(emp_r)+" empty "+str(fil_r)+" filled, total lenght "+str(len(MJD_ro))
        print "V "+str(emp_v)+" empty "+str(fil_v)+" filled, total lenght "+str(len(MJD_vo))
        #plt.show()
        
        if str(len(MJD_bo)) > '0' :
            print "print"
            outbprint = numpy.stack((MJD_bo,ZP_bo,ZPERR_bo,FLUXAGN_bo,FLUXERR_bo,MagAGN_bo,MagerrAGN_bo),axis = -1)
            
            numpy.savetxt(str(Obj[i]+"_B_"+str(CAT[i])+"_allData.data"),numpy.asarray(outbprint) , delimiter="\t",fmt = '%s',header = ('MJD'+'\t'+'ZP'+'\t'+'ZPERR'+'\t'+'FLUX'+'\t'+'FLUXERR'+'\t'+'MAG'+'\t'+'MAGERR'))
        else:
            #print "No print"
            pass

        if str(len(MJD_ro)) > '0' :
            print "print"
            outrprint = numpy.stack((MJD_ro,ZP_ro,ZPERR_ro,FLUXAGN_ro,FLUXERR_ro,MagAGN_ro,MagerrAGN_ro),axis = -1)
            
            numpy.savetxt(str(Obj[i]+"_R_"+str(CAT[i])+"_allData.data"),numpy.asarray(outrprint) , delimiter="\t",fmt = '%s',header = ('MJD'+'\t'+'ZP'+'\t'+'ZPERR'+'\t'+'FLUX'+'\t'+'FLUXERR'+'\t'+'MAG'+'\t'+'MAGERR'))
        else:
            #print "No print"
            pass
        
        if str(len(MJD_vo)) > '0' :
            print "print"
            outvprint = numpy.stack((MJD_vo,ZP_vo,ZPERR_vo,FLUXAGN_vo,FLUXERR_vo,MagAGN_vo,MagerrAGN_vo),axis = -1)
            
            numpy.savetxt(str(Obj[i]+"_V_"+str(CAT[i])+"_allData.data"),numpy.asarray(outvprint) , delimiter="\t",fmt = '%s',header = ('MJD'+'\t'+'ZP'+'\t'+'ZPERR'+'\t'+'FLUX'+'\t'+'FLUXERR'+'\t'+'MAG'+'\t'+'MAGERR'))
        else:
            #print "No print"
            pass
            
        print "----------"

outfile.close()


os.system("mv *allData.data  All_data")
