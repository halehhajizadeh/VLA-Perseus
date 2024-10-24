# First index is Stokes
# Second index is frequency
# Third index is DEC
# Fourth index is RA
import sys
sys.path.append('.')
from configs import path, nit
import os
import numpy as np
from casatools import image as ia  # CASA's image tool

# Updated path with mosaic name (specific_dirs)
specific_dirs = '03:32:04.530001_+31.05.04.00000/'  # As used in your previous scripts
# specific_dirs =  '03:36:00.000000_+30.30.00.00001/' 
# specific_dirs =  '03:34:30.000000_+31.59.59.99999/'
# specific_dirs =  '03:25:30.000000_+29.29.59.99999/'
# specific_dirs =  '03:23:30.000001_+31.30.00.00000/'

path = os.path.join(path, "concat", specific_dirs)

stokes_list = ['I', 'Q', 'U']

# Function to create an empty channel FITS file using CASA tools
def create_empty_channel(fitsname):
    flagged_channel = os.path.join(path, f'Images/img{nit}/fits/empty_channel.fits')

    # Remove existing empty channel file if it exists
    syscommand = f'rm -rf {flagged_channel}'
    os.system(syscommand)

    # Open the image using CASA's image tool
    ia.open(fitsname)
    img_fits = ia.getchunk()  # Retrieve the image data
    img_fits[:] = np.nan  # Set all data to NaN

    # Create the empty channel FITS file
    ia.putchunk(img_fits)
    ia.tofits(flagged_channel, overwrite=True)
    ia.close()
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
    syscommand = f'rm -rf {cubename}'
    os.system(syscommand)

    # Read the list of FITS files for the current Stokes parameter
    with open(os.path.join(path, f'Images/img{nit}/Stokes{stokes}.txt'), 'r') as f:
        file_list = f.read().splitlines()

    # Remove any leading empty channel files from the list
    file_list = remove_empty_channel_from_start(file_list)

    # Adding the first channel to the list and initializing the cube
    inputfile = file_list[0]
    ia.open(inputfile)
    img = ia.getchunk()  # Get the data for the first channel
    cube = np.copy(img[:, :, :, :])  # Copy it to initialize the cube

    # Create an empty channel FITS file
    create_empty_channel(inputfile)
    print('Empty channel is produced!')

    # Loop through the file list, appending data to the cube
    for filename in file_list:
        ia.open(filename)
        imgCP = ia.getchunk()
        if filename == os.path.join(path, f'Images/img{nit}/fits/empty_channel.fits'):
            # Replace NaN values with 1e30 to avoid issues
            imgCP[np.isnan(imgCP)] = 1e30
        img2cube = np.copy(imgCP[:, :, :, :])
        cube = np.append(cube, img2cube, axis=0)
        ia.close()

    print('For loop completed!')

    # Save the completed cube to the output FITS file
    ia.open(inputfile)
    ia.putchunk(cube)
    ia.tofits(cubename, overwrite=True)
    ia.close()

    print(f'Making cube for Stokes {stokes} is done!')
