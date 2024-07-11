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

        image = base_directory + data + subdir_t + "spw" + str(s) + "-2.5arcsec-nit" + str(nit) + "-" + '-awproject.image.tt0'
        smo = base_directory + data + subdir_s + "spw" + str(s) + "-2.5arcsec-nit" + str(nit) + "-" + '-awproject.smo'
        fits = base_directory + data + subdir_f + "spw" + str(s) + "-2.5arcsec-nit" + str(nit) + "-" + '-awproject.fits'
        print(image)

        # Check if smo file exists and delete if it does
        if os.path.exists(smo):
            os.remove(smo)
            print(f"Deleted existing file: {smo}")

        # Check if fits file exists and delete if it does
        if os.path.exists(fits):
            os.remove(fits)
            print(f"Deleted existing file: {fits}")

        imsmooth(imagename=image,
                 targetres=True,
                 major='55arcsec',
                 minor='43arcsec',
                 pa='0.0deg',
                 outfile=smo,
                 overwrite=True
                 )

        exportfits(
            imagename=smo,
            fitsimage=fits
        )
