import sys
sys.path.append('.')
import time
import os
import numpy as np

thresh = '2e-4'
pblim = -0.001
nit = 5000

# phase_center = 'J2000 03:32:04.530001 +31.05.04.00000'
# phase_center = 'J2000 03:36:00.000000 +30.30.00.00001'
# phase_center = 'J2000 03:25:30.000000 +29.29.59.99999'
phase_center = 'J2000 03:23:30.000001 +31.30.00.00000'


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

# mosaic_name = '03:32:04.530001_+31.05.04.00000'
# mosaic_name = '03:36:00.000000_+30.30.00.00001' 
# mosaic_name = '03:25:30.000000_+29.29.59.99999'
mosaic_name = '03:23:30.000001_+31.30.00.00000'



base_directory = '../data/' + mosaic_name

# Get the list of calibrated files
ms_file_list = find_calibrated_files(base_directory)

# Print the list of calibrated files
print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
for file in ms_file_list:
    print(file)
print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')

#----------------------------------------------------------------



img_filename =  "../data/concat/total/ALL/tclean/" + str(mosaic_name) +  "spwALL" + "-2.5arcsec-nit" + str(nit) + "-" + '-awproject'

tclean( vis=ms_file_list,
        field="PER_FIELD_*",
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
        cfcache=f'/dev/shm/{mosaic_name}.cf',
        pblimit=pblim,
        deconvolver="mtmfs",
        pbcor=True,
        weighting="briggs",
        robust=0.5,
        niter=nit,
        gain=0.1,
        threshold=thresh,
        nsigma=3,
        # cycleniter=200,
        cyclefactor=1,
        parallel=True,
        # psterm=True,
        nterms=2,
        rotatepastep=5.0,
        interactive=False,
        )

############################################################################################

