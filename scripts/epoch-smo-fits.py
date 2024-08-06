import os
import glob  # For handling wildcard file paths
import shutil  # For file operations

# Constants
NIT = 5000
BASE_DIRECTORY = '../data/epoch/'

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
    # Generate file paths
    image_pattern = os.path.join(BASE_DIRECTORY, data, SUBDIR_T, '*.image.tt0')
    smo_pattern = os.path.join(BASE_DIRECTORY, data, SUBDIR_S, '*.image.tt0.smo')
    fits_pattern = os.path.join(BASE_DIRECTORY, data, SUBDIR_F, '*.image.tt0.smo.fits')

    image_files = glob.glob(image_pattern)
    smo_files = glob.glob(smo_pattern)
    fits_files = glob.glob(fits_pattern)

    for image_file in image_files:
        smo_file = image_file + '.smo'
        fits_file = smo_file + '.fits'

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
            major='45arcsec',
            minor='45arcsec',
            pa='0.0deg',
            outfile=smo_file,
            overwrite=True
        )

        # Export to FITS format
        exportfits(
            imagename=smo_file,
            fitsimage=fits_file
        )
