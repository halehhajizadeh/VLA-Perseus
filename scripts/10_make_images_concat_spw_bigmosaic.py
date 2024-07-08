import sys
sys.path.append('.')
import time
import os
import numpy as np

thresh = '2e-4'
pblim = -0.01
nit = 6000
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
phase_center = 'J2000 03:28:41.5 +30.49.48.0'


def find_calibrated_files(base_directory, specific_dirs):
    calibrated_files = []

    for directory in specific_dirs:
        full_path = os.path.join(base_directory, directory)
        if os.path.exists(full_path) and os.path.isdir(full_path):
            products_path = os.path.join(full_path, 'products')
            if os.path.exists(products_path):
                for file in os.listdir(products_path):
                    if file.startswith('19B-053') and file.endswith('_calibrated.ms'):
                        calibrated_files.append(os.path.join(products_path, file))

    return calibrated_files

# Example usage
base_directory = '../data/'
specific_dirs = [
    '03:23:30.000001_+31.30.00.00000/',  
    '03:32:04.530001_+31.05.04.00000/',  
    '03:36:00.000000_+30.30.00.00001/',  
    '03:25:30.000000_+29.29.59.99999/'
]

calibrated_files = find_calibrated_files(base_directory, specific_dirs)

# Print the list of calibrated files
for file in calibrated_files:
    print(file)



# Specify the base directory
mosaic_name = 'bigmosaic/'
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

