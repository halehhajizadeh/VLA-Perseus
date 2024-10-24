#!!!!!!!!!!!!!!!!!!!!!!!!!!RUN IT IN NMPOST_MASTER AND OUT OF CASA!!!!!!!!!!!!!!!!!!!!!!!!!!

# First index is Stokes
# Second index is frequency
# Third index is DEC
# Fourth index is RA
import sys
sys.path.append('.')
import os
import numpy as np
from astropy.io import fits  # Keep astropy for handling FITS files


nit=5000

# Updated path with mosaic name (specific_dirs)
# specific_dirs = '03:32:04.530001_+31.05.04.00000/'  # As used in your previous scripts
specific_dirs =  '03:36:00.000000_+30.30.00.00001/'
# specific_dirs =  '03:34:30.000000_+31.59.59.99999/'
# specific_dirs =  '03:25:30.000000_+29.29.59.99999/'
# specific_dirs =  '03:23:30.000001_+31.30.00.00000/'

# Update path to use mosaic name and concat directory
base_path = '../data/concat/'  # Assuming this is the base path as used before
path = os.path.join(base_path, specific_dirs)

# Modify niter as per request (change this to your desired value)
nit = 5000  # Example new niter value, adjust as per your needs

stokes_list = ['I', 'Q', 'U']

# Function to create an empty channel FITS file using astropy
def create_empty_channel(fitsname):
    flagged_channel = os.path.join(path, f'Images/img{nit}/fits/empty_channel.fits')

    # Remove existing empty channel file if it exists
    if os.path.exists(flagged_channel):
        os.remove(flagged_channel)

    # Open the FITS file, set all data to NaN, and create the empty channel
    with fits.open(fitsname) as hdul:
        img_fits = hdul[0].data
        img_fits[:] = np.nan  # Set all data to NaN
        hdul.writeto(flagged_channel, overwrite=True)

    return flagged_channel

# Function to remove empty channels from the start of the file list
def remove_empty_channel_from_start(filelist):
    if not filelist:
        return []
    if "empty_channel.fits" not in filelist[0]:
        return filelist
    else:
        return remove_empty_channel_from_start(filelist[1:])

# Process for each Stokes parameter
for stokes in stokes_list:
    cubename = os.path.join(path, f'Images/img{nit}/Stokes{stokes}.fits')

    # Remove any existing cube file
    if os.path.exists(cubename):
        os.remove(cubename)

    # Read the list of FITS files for the current Stokes parameter
    with open(os.path.join(path, f'Images/img{nit}/Stokes{stokes}.txt'), 'r') as f:
        file_list = f.read().splitlines()

    # Remove any leading empty channel files from the list
    file_list = remove_empty_channel_from_start(file_list)

    # Adding the first channel to the list and initializing the cube
    inputfile = file_list[0]
    with fits.open(inputfile) as hdulist:
        img = hdulist[0].data
        cube = np.copy(img[0, :, :, :])  # Copy it to initialize the cube

    # Create an empty channel FITS file
    create_empty_channel(inputfile)
    print('Empty channel is produced!')

    # Loop through the file list, appending data to the cube
    for filename in file_list:
        with fits.open(filename) as hdulistCP:
            imgCP = hdulistCP[0].data
            if filename == os.path.join(path, f'Images/img{nit}/fits/empty_channel.fits'):
                # Replace NaN values with 1e30 to avoid issues
                imgCP[np.isnan(imgCP)] = 1e30
            img2cube = np.copy(imgCP[0, :, :, :])
            cube = np.append(cube, img2cube, axis=0)

    print('For loop completed!')

    # Save the completed cube to the output FITS file
    hdulist[0].data = cube
    hdulist.writeto(cubename, overwrite=True)

    print(f'Making cube for Stokes {stokes} is done!')
