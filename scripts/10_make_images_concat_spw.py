import sys
sys.path.append('.')
import time
import os
import numpy as np

thresh = '2e-4'
pblim = -0.001
nit = 5000
spw = [
       2,
       3 , 
       4, 
       5, 
       6, 
       8, 
       15, 
       16, 
       17
       ]
phase_center = 'J2000 03:34:30.000000 +31.59.59.99999'

fields = 'PER_FIELD_1, PER_FIELD_3, PER_FIELD_4, PER_FIELD_2, PER_FIELD_6, PER_FIELD_5, PER_FIELD_11,\
PER_FIELD_10, PER_FIELD_17, PER_FIELD_8, PER_FIELD_7, PER_FIELD_13, PER_FIELD_12, PER_FIELD_19,\
PER_FIELD_18, PER_FIELD_26, PER_FIELD_35, PER_FIELD_27, PER_FIELD_28, PER_FIELD_20, PER_FIELD_21,\
PER_FIELD_14,'

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
mosaic_name = '03:34:30.000000_+31.59.59.99999/'
base_directory = '../data/' + mosaic_name

# Get the list of calibrated files
ms_file_list = find_calibrated_files(base_directory)

# Print the list of calibrated files
print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
for file in ms_file_list:
    print(file)
print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')

#----------------------------------------------------------------


for s in spw:
    tic = time.time()
    print(f"Stokes: I, s: {s} is started ...")

    img_filename =  "../data/concat/total/" + mosaic_name + "tclean/" +  "spw" + str(s) + "-2.5arcsec-nit" + str(nit) + "-" + '-awproject'

    tclean( vis=ms_file_list,
            field="PER_FIELD_*",
            spw=str(s),
            timerange="",
            uvrange="",
            antenna="",
            observation="",
            intent="",
            datacolumn="corrected",
            imagename=img_filename,
            imsize=[4096],
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
            threshold=thresh,
            # nsigma=3,
            # cycleniter=200,
            cyclefactor=1,
            parallel=True,
            # psterm=True,
            nterms=2,
            rotatepastep=5.0,
            interactive=False,
            )

    toc = time.time()
    print(f"stokesI, s: {s} is finished!")
    print(f"Finshed the process in {round((toc-tic)/60)} minutes")


############################################################################################

