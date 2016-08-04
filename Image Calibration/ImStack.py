#python Stacking and Source extraction program from Skynet Prompt8 telescope and hes catalog. written by bovornpratch Vijarnwannaluk on June 21st 2016
import numpy
import os
import libastro as LA
import sys
import glob

CURRENT_DIR = os.path.dirname(__file__)

oldfiles =  os.path.join(CURRENT_DIR,"HE*.fits")
os.system("rm "+oldfiles)
oldpathco =  os.path.join(CURRENT_DIR,"coadd.fits")
oldpathweight =  os.path.join(CURRENT_DIR,"w.weight.fits")
os.system("rm "+oldpathco)
os.system("rm "+oldpathweight)



Bin  =  sys.argv[1]

searchField = "*.fits"
file_path_glob = os.path.join(CURRENT_DIR, str(searchField))
imagebay = []
search = glob.glob(file_path_glob)
for i in range(0,len(search)):
    if "hes_sample_monitoring.fits" in str(search[i]) or "_S.fits" in str(search[i]):
        continue
    else:
        imagebay.append(str(search[i]))
        

file_path_ref = os.path.join(CURRENT_DIR,"Pipeline.param" )
parameter = numpy.genfromtxt(file_path_ref, unpack = True, dtype = None)
keys,values  = parameter[0], parameter[1]
objname = str(values[0])
RA =  str(values[1])
DEC = str(values[2])
Filter = str(values[3])
obsID = str(values[4])

binsize = float(Bin) - 0.5

Output_temp = objname+"_"+obsID+"_"+Filter
print "Output Template"+'\t'+str(Output_temp)

#RawFiles = LA.GetFits(NameKey)# call all fits file
RawFiles = numpy.array(imagebay)
RefFile = LA.FirstFile(RawFiles)

print "Object is"+'\t'+str(objname)
print "Observation Number "+ str(obsID)
print "binning size is "+str(binsize)+" days"
print "using", RefFile ,"as Reference"

MJD_sort = LA.ObtainMJDs(RawFiles)            #obtain MJD for all days
MJD_sort = numpy.array(MJD_sort)
MJD_key = numpy.argsort(MJD_sort)

MJD_list = MJD_sort[MJD_key]
print MJD_key
RawFiles = RawFiles[MJD_key]

file_path_SWARP = os.path.join(CURRENT_DIR,'SwarpList.txt' )
outtable1 = open(file_path_SWARP,'w')

file_array_re =[]
MJD_array_re =[]
done = []
print "++++"

file_path_default = os.path.join(CURRENT_DIR,'default.swarp' )
file_path_Nametemp = os.path.join(CURRENT_DIR,"NAME_TEMP.txt" )

for i in range(0,len(MJD_list)):
    if RawFiles[i] in done:
        continue
    else:
        #print str(i)+'\t'+str(RawFiles[i])+'\t'+str(MJD_list[i])
        swarp_in = open(file_path_Nametemp,'w')
        temp = []
        temp_MJD = []
    
        done.append(RawFiles[i])
        temp.append(RawFiles[i])
        temp_MJD.append(MJD_list[i])
        
    #print MJD_list
   
    for j in range(0,len(MJD_list)):
        timediff =  MJD_list[j] - MJD_list[i]
        if timediff > 0 and timediff < binsize and RawFiles[j] not in done :
            #print  timediff ,  "ok"
            done.append(RawFiles[j])
            temp.append(RawFiles[j])
            temp_MJD.append(MJD_list[j])
        else:
            continue
    print temp
    print "---"
    Newname = Output_temp+"_"+str(temp_MJD[0])+"_S.fits"
    file_path_NewName = os.path.join(CURRENT_DIR,Newname )

    file_array_re.append(Newname)
    print>>outtable1,str(Newname)+'\t'+str(temp_MJD[0])
     
    print "Stacking to one file"
    for k in range(0,len(temp)):
        print str(temp[k])+'\t'+str(temp_MJD[k])
        print>>swarp_in, temp[k]
        print>>outtable1, str(temp[k])+'\t'+str(temp_MJD[k])
    print>>outtable1, "--------------------"
    
    MJD_array_re.append(temp_MJD[0])
    swarp_in.close()
    print "Output as"
    print str(Newname)+'\t'+str(temp_MJD[0])
    os.system("swarp @"+file_path_Nametemp+" -c "+file_path_default)
    LA.Rename("~/Desktop/Workspace/coadd.fits",file_path_NewName)        
    
file_path_rmname = os.path.join(CURRENT_DIR,"NAME_TEMP.txt")
os.system("rm "+file_path_rmname)
print "------------------------SUMMERY------------------------------"
print "file name"+'\t'+'\t'+'\t'+'\t'+'\t'"MJD"

file_path_out = os.path.join(CURRENT_DIR,"Input_"+str(Output_temp)+".txt" )
export = open(file_path_out,'w')
print>>export,"#Imagefile"+'\t'+"MJD"

for i in range(0,len(file_array_re)):
    
    print str(file_array_re[i])+'\t'+str(MJD_array_re[i])
    print>>export, str(file_array_re[i])+'\t'+str(MJD_array_re[i])
            
export.close()        
