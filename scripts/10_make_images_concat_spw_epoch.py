import sys
sys.path.append('.')
import time
import os
import numpy as np

path = '../data'
thresh = '2e-4'
pblim = -0.001  # Ensure pblim is positive
nit = 5000

# phase_center = 'J2000 03:32:04.530001 +31.05.04.00000'
phase_center = 'J2000 03:36:00.000000 +30.30.00.00001'
# phase_center = 'J2000 03:34:30.000000 +31.59.59.99999'
# phase_center = 'J2000 03:25:30.000000 +29.29.59.99999'
# phase_center = 'J2000 03:23:30.000001 +31.30.00.00000'

# specific_dirs = '03:32:04.530001_+31.05.04.00000/'
specific_dirs =  '03:36:00.000000_+30.30.00.00001/' 
# specific_dirs =  '03:34:30.000000_+31.59.59.99999/'
# specific_dirs =  '03:25:30.000000_+29.29.59.99999/'
# specific_dirs =  '03:23:30.000001_+31.30.00.00000/'

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
base_directory = os.path.join('..', 'data', specific_dirs, 'data')

# Get the list of calibrated files
ms_file_list = find_calibrated_files(base_directory)

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
base_directory = os.path.join('..', 'data', specific_dirs, 'data')

# Get the list of calibrated files
ms_file_list = find_calibrated_files(base_directory)

# Print the list of calibrated files
print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
for file in ms_file_list:
    print(file)
print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')

#----------------------------------------------------------------

for ms in ms_file_list:
    print('================================================================')
    print(ms)
 
    tic = time.time()
    print(f"Stokes: I, folder: {ms} is started ...")

    img_filename = os.path.join("..", "data", "epoch", specific_dirs, "tclean", f"ms-2.5arcsec-nit{nit}-awproject")

    tclean(vis=ms,
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
    print(f"Finished the process in {round((toc-tic)/60)} minutes")

############################################################################################

for ms in ms_file_list:
    print('================================================================')
    print(ms)
 
    tic = time.time()
    print(f"Stokes: I, folder: {ms} is started ...")
    
    imagename = os.path.join("..", "data", "epoch", specific_dirs, "tclean", f"ms-2.5arcsec-nit{nit}-awproject.image")
    fitsimage = os.path.join("..", "data", "epoch", specific_dirs, "fits", f"ms-2.5arcsec-nit{nit}-awproject.image.fits")

    exportfits(imagename=imagename, fitsimage=fitsimage)

    toc = time.time()
    print(f"Finished the export in {round((toc-tic)/60)} minutes")
