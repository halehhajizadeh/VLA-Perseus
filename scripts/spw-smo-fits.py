import sys
sys.path.append('.')
import os
import time

spw = [2, 3, 4, 5, 6, 8, 15, 16, 17]
nit = 5000

base_directory = '../data/concat/total/'

specific_dirs = [
    '03:23:30.000001_+31.30.00.00000/',
    '03:32:04.530001_+31.05.04.00000/',
    '03:36:00.000000_+30.30.00.00001/',
    '03:25:30.000000_+29.29.59.99999/',
    # '03:34:30.000000_+31.59.59.99999/'
]

subdir_t = 'tclean/'
subdir_s = 'smo/'
subdir_f = 'fits/'

for data in specific_dirs:
    for s in spw:

        image_file = base_directory + data + subdir_t + "spw" + str(s) + "-2.5arcsec-nit" + str(nit) + "-" + '-awproject.image.tt0'
        smo_file = base_directory + data + subdir_s + "spw" + str(s) + "-2.5arcsec-nit" + str(nit) + "-" + '-awproject.smo'
        fits_file = base_directory + data + subdir_f + "spw" + str(s) + "-2.5arcsec-nit" + str(nit) + "-" + '-awproject.fits'
        print(image_file)

        # Check if smo path is a file and delete if it does
        if os.path.isfile(smo_file):
            os.remove(smo_file)
            print(f"Deleted existing file: {smo_file}")

        # Check if fits path is a file and delete if it does
        if os.path.isfile(fits_file):
            os.remove(fits_file)
            print(f"Deleted existing file: {fits_file}")

        imsmooth(imagename=image_file,
                 targetres=True,
                 major='60arcsec',
                 minor='60arcsec',
                 pa='0.0deg',
                 outfile=smo_file,
                 overwrite=True
                 )

        exportfits(
            imagename=smo_file,
            fitsimage=fits_file
        )