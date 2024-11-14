import sys
sys.path.append('.')
import os
import numpy as np
from astropy.io import fits

# Define parameters
specific_dirs = '03:32:04.530001_+31.05.04.00000/'
# specific_dirs = '03:36:00.000000_+30.30.00.00001/'
# specific_dirs = '03:25:30.000000_+29.29.59.99999/'
# specific_dirs = '03:23:30.000001_+31.30.00.00000/'



base_path = '../data/concat/'
path = os.path.join(base_path, specific_dirs)
nit = 5000
stokes_list = ['I', 'Q', 'U']
# Subtract 1 from each index in drop_indices to adjust replacement positions
# #32
drop_indices = {
    'I': [i - 1 for i in [41, 45, 48, 49, 53, 80, 95]],
    'Q': [i - 1 for i in [41, 45, 48, 49, 53, 80, 95]],
    'U': [i - 1 for i in [41, 45, 48, 49, 53, 80, 95]]
}
# #36
# drop_indices = {
#     'I': [i - 1 for i in [41, 42, 48, 49, 80]],
#     'Q': [i - 1 for i in [41, 42, 48, 49, 80]],
#     'U': [i - 1 for i in [41, 42, 48, 49, 80]]
# }

# # 25
# drop_indices = {
#     'I': [i - 1 for i in [41, 48, 49, 79, 80]],
#     'Q': [i - 1 for i in [41, 48, 49, 79, 80]],
#     'U': [i - 1 for i in [41, 48, 49, 79, 80]]
# }

# # 23
# drop_indices = {
#     'I': [i - 1 for i in [41, 48, 49, 80]],
#     'Q': [i - 1 for i in [41, 48, 49, 80]],
#     'U': [i - 1 for i in [41, 48, 49, 80]]
# }


# Function to create an empty channel FITS file
def create_empty_channel(fitsname):
    flagged_channel = os.path.join(path, f'Images/img{nit}/fits/empty_channel.fits')
    if os.path.exists(flagged_channel):
        os.remove(flagged_channel)

    with fits.open(fitsname) as hdul:
        img_fits = hdul[0].data
        img_fits[:] = np.nan
        hdul.writeto(flagged_channel, overwrite=True)

    return flagged_channel

# Process each Stokes parameter
for stokes in stokes_list:
    cubename = os.path.join(path, f'Images/img{nit}/Stokes{stokes}.fits')
    if os.path.exists(cubename):
        os.remove(cubename)

    # Load the Stokes file list
    with open(os.path.join(path, f"Images/img{nit}/Stokes{stokes}.txt"), 'r') as f:
        file_list = f.read().splitlines()
    print(f'Processing Stokes {stokes}: Found {len(file_list)} files.')

    inputfile = file_list[0]
    with fits.open(inputfile) as hdulist:
        img = hdulist[0].data
        cube = np.copy(img[0, :, :, :])

    empty_channel_file = create_empty_channel(inputfile)
    print('Empty channel is produced!')

    # Loop through file_list and add to the cube
    for file_index, filename in enumerate(file_list):
        # Adjust the replacement based on modified drop_indices
        if file_index in drop_indices.get(stokes, []):
            filename = empty_channel_file
            print(f"Replacing index {file_index} with empty channel for Stokes {stokes}")

        with fits.open(filename) as hdulistCP:
            imgCP = hdulistCP[0].data
            if filename == empty_channel_file:
                imgCP[np.isnan(imgCP)] = 1e30
            img2cube = np.copy(imgCP[0, :, :, :])
            cube = np.append(cube, img2cube, axis=0)

        print(f"Added file {filename} to cube at index {file_index}")

    print(f"Cube completed for Stokes {stokes}")

    try:
        hdulist[0].data = cube
        hdulist.writeto(cubename, overwrite=True)
        print(f"Cube saved for Stokes {stokes} at {cubename}")
    except Exception as e:
        print(f"Error saving cube for {stokes}: {e}")

