import sys
sys.path.append('.')
import time
import os
import numpy as np

thresh = '2e-4'
pblim = 0.001
nit = 5000
spw = [
    #    2,
    #    3 , 
    #    4, 
    #    5, 
    #    6, 
    #    8, 
    #    15, 
       16, 
    #    17
       ]

def find_calibrated_files(base_directory):
    calibrated_files = []

    # Traverse through all directories and subdirectories
    for root, dirs, files in os.walk(base_directory):
        for directory in dirs:
            if directory.startswith('19B-053'):
                products_path = os.path.join(root, directory, 'products')
                if os.path.exists(products_path):
                    for file in os.listdir(products_path):
                        if file.startswith('19B-053') and file.endswith('_calibrated.ms'):
                            calibrated_files.append(os.path.join(products_path, file))

    return calibrated_files

# Specify the base directory
base_directory = '../data/'

# Get the list of calibrated files
ms_file_list = find_calibrated_files(base_directory)

# Print the list of calibrated files
for file in ms_file_list:
    print(file)


#----------------------------------------------------------------


for s in spw:
    tic = time.time()
    print(f"Stokes: I, s: {s} is started ...")

    img_filename = path + "/concat/total/Images/img" + str(nit) + "/tclean/" +  "4-spw" + str(s) + "-2.5arcsec-nit" + str(nit) + "-" + str(thresh) + '-awproject'

    tclean( vis=ms_file_list,
            field="PER_FIELD_*, J0336+3218",
            spw=str(s),
            timerange="",
            uvrange="",
            antenna="",
            observation="",
            intent="",
            datacolumn="corrected",
            imagename=img_filename,
            imsize=[10000],
            cell="2.5arcsec",
            # phasecenter=phase_center,
            stokes='I',
            # projection="SIN",
            specmode="mfs",
            gridder="awproject",
            mosweight=True,
            # cfcache="",
            pblimit=pblim,
            # normtype="flatnoise",
            deconvolver="mtmfs",
            # restoration=True,
            # restoringbeam=[],
            pbcor=True,
            # outlierfile="",
            weighting="briggs",
            robust=0.5,
            # npixels=0,
            niter=nit,
            gain=0.1,
            threshold=thresh,
            nsigma=0,
            cycleniter=200,
            cyclefactor=1,
            parallel=True,
            psterm=True,
            nterm=2,
            rotatepastep=5.0,
            interactive=True,
            )

    toc = time.time()
    print(f"stokesI, s: {s} is finished!")
    print(f"Finshed the process in {round((toc-tic)/60)} minutes")


############################################################################################

for s in spw:
    exportfits(
        imagename =  base_directory + "concat/total/Images/img" + str(nit) + "/tclean/" +  "16-spw" + str(s) + "-2.5arcsec-nit" + str(nit) + "-" + str(thresh) + '-awproject' + '.image',
        fitsimage =  base_directory + "concat/total/Images/img" + str(nit) + "/fits/" +  "16-spw" + str(s) + "-2.5arcsec-nit" + str(nit) + "-" + str(thresh) + '-awproject' + '.image.fits'           
    )
