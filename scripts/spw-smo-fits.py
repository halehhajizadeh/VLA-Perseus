import sys
import os
import glob  # For handling wildcard file paths
import shutil  # For file operations

# Append current directory to system path
sys.path.append('.')

# Constants
SPW = [2, 3, 4, 5, 6, 8, 15, 16, 17]
NIT = 5000
BASE_DIRECTORY = '../data/concat/total/'

SPECIFIC_DIRS = [
    '03:23:30.000001_+31.30.00.00000/',
    '03:32:04.530001_+31.05.04.00000/',
    '03:36:00.000000_+30.30.00.00001/',
    '03:25:30.000000_+29.29.59.99999/',
    # '03:34:30.000000_+31.59.59.99999/'  # Uncomment if needed
]

SUBDIR_T = 'tclean/'
SUBDIR_S = 'smo/'
SUBDIR_F = 'fits/'

for data in SPECIFIC_DIRS:
    for s in SPW:
        # Generate file paths
        image_file = os.path.join(BASE_DIRECTORY, data, SUBDIR_T, f"spw{s}-2.5arcsec-nit{NIT}--awproject.image.tt0")
        smo_file = os.path.join(BASE_DIRECTORY, data, SUBDIR_S, f"spw{s}-2.5arcsec-nit{NIT}-awproject.smo")
        fits_file = os.path.join(BASE_DIRECTORY, data, SUBDIR_F, f"spw{s}-2.5arcsec-nit{NIT}-awproject.fits")
        
        print(f"Processing {image_file}")

        # Delete existing smo file if it exists
        if os.path.isfile(smo_file):
            os.remove(smo_file)
            print(f"Deleted existing file: {smo_file}")

        # Delete existing fits file if it exists
        if os.path.isfile(fits_file):
            os.remove(fits_file)
            print(f"Deleted existing file: {fits_file}")

        # Perform image smoothing
        imsmooth(
            imagename=image_file,
            targetres=True,
            major='60arcsec',
            minor='60arcsec',
            pa='0.0deg',
            outfile=smo_file,
            overwrite=True
        )

        # Export to FITS format
        exportfits(
            imagename=smo_file,
            fitsimage=fits_file
        )
