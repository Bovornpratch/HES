import os
import glob
import sys

CURRENT_DIR = os.path.dirname(__file__)


Name = str(sys.argv[1])
Filter =str(sys.argv[2])

Area = 30
Num = 5000
lowlim = 12
highlim = 16

Calib_File = glob.glob(os.path.join(CURRENT_DIR,"Input*QC.txt"))
Catalog = os.path.join(CURRENT_DIR,"LiveStar.list")

#ELLIP = 0.5
#FWHM_MAX = 0.005
#SigClipLim = 1
#factor = 2

ELLIP = float(sys.argv[3])
FWHM_MAX = float(sys.argv[4])
SigClipLim = float(sys.argv[5])
factor = float(sys.argv[6])
#-----------------------------------------------------------------

file_path_Photo = os.path.join(CURRENT_DIR,"Photometry_Param_Setup.py")
file_path_CAT = os.path.join(CURRENT_DIR,"Get_Catalog_SDSS.py")
file_path_SS = os.path.join(CURRENT_DIR,"StarSelection.py")
file_path_calib = os.path.join(CURRENT_DIR,"Calibration.py")

#------------------------------------------------------------------

os.system("python "+file_path_Photo+" "+str(Name)+" "+str(Filter))
os.system("python "+file_path_CAT+" "+str(Area)                                                                  +" "+str(Num)                                                                   +" "+str(lowlim)                                                                +" "+str(highlim))
os.system("python "+file_path_SS+" "+str(Calib_File[0]))

os.system("python "+file_path_calib+" "+str(Calib_File[0])+" "+str(Catalog)                                        +" "+str(ELLIP)                                                                 +" "+str(FWHM_MAX)                                                              +" "+str(SigClipLim)                                                            +" "+str(factor))
