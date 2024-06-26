import sys
sys.path.append('.')
import time
import os
import numpy as np

# thresh = '1e-4'
pblim = -0.001
nit = 6500
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
# phase_center = 'J2000 03:32:04.530001 +31.05.04.00000'
phase_center='J2000 03:28:27.7 +30.26.17.00000'

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

    img_filename = base_directory + "concat/total/Images/img" + str(nit) + "/tclean/" +  "spw" + str(s) + "-2.5arcsec-nit" + str(nit) + "-" + '-awproject'

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
            phasecenter=phase_center,
            stokes='I',
            specmode="mfs",
            gridder="awproject",
            mosweight=True,
            # cfcache="",
            pblimit=pblim,
            deconvolver="mtmfs",
            pbcor=True,
            weighting="briggs",
            robust=0.5,
            niter=nit,
            gain=0.1,
            # threshold=thresh,
            nsigma=3,
            cycleniter=200,
            cyclefactor=1,
            parallel=True,
            psterm=True,
            nterms=2,
            rotatepastep=5.0,
            interactive=False,
            )

    toc = time.time()
    print(f"stokesI, s: {s} is finished!")
    print(f"Finshed the process in {round((toc-tic)/60)} minutes")


############################################################################################

