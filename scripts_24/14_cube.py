import sys
sys.path.append('.')
import os
import numpy as np
from astropy.io import fits

# === Parameters ===
nit = 4000
stokes_list = ['I', 'Q', 'U']

# === Choose ONE mosaic name to activate ===
mosaic_name = '03:26:24.057_+30.35.58.881'
# mosaic_name = '03:29:12.973_+31.48.05.579'
# mosaic_name = '03:31:12.055_+29.47.58.916'
# mosaic_name = '03:39:12.060_+31.23.58.844'
# mosaic_name = '03:40:00.063_+32.23.58.799'
# mosaic_name = '03:42:00.057_+30.29.58.885'
# mosaic_name = '03:45:12.060_+31.41.58.831'
# mosaic_name = '03:45:36.064_+32.47.58.780'

concat_base = f'/lustre/aoc/observers/nm-12934/VLA-Perseus/data/new/data/concat/{mosaic_name}'

# === Drop indices for flagged channels (adjust per mosaic as needed) ===
# Subtract 1 from each index to adjust replacement positions
drop_indices = {
    'I': [i - 1 for i in []],
    'Q': [i - 1 for i in []],
    'U': [i - 1 for i in []]
}

# === Function to create an empty channel FITS file ===
def create_empty_channel(fitsname, output_path):
    flagged_channel = os.path.join(output_path, 'empty_channel.fits')
    if os.path.exists(flagged_channel):
        os.remove(flagged_channel)

    with fits.open(fitsname) as hdul:
        img_fits = hdul[0].data
        img_fits[:] = np.nan
        hdul.writeto(flagged_channel, overwrite=True)

    return flagged_channel

# === Setup directories ===
img_dir = f"{concat_base}/Images/img"

# === Main loop to process each Stokes parameter ===
for stokes in stokes_list:
    cubename = os.path.join(img_dir, f'Stokes{stokes}.fits')
    if os.path.exists(cubename):
        os.remove(cubename)

    # Load the Stokes file list
    stokes_list_file = os.path.join(img_dir, f"Stokes{stokes}.txt")
    if not os.path.exists(stokes_list_file):
        print(f"WARNING: {stokes_list_file} not found, skipping Stokes {stokes}")
        continue

    with open(stokes_list_file, 'r') as f:
        file_list = f.read().splitlines()
    print(f'\nProcessing Stokes {stokes}: Found {len(file_list)} files.')

    if len(file_list) == 0:
        print(f"WARNING: No files found for Stokes {stokes}, skipping")
        continue

    inputfile = file_list[0]
    if not os.path.exists(inputfile) or 'empty_channel' in inputfile:
        print(f"WARNING: First file not valid: {inputfile}, skipping Stokes {stokes}")
        continue

    with fits.open(inputfile) as hdulist:
        img = hdulist[0].data
        cube = np.copy(img[0, :, :, :])

    empty_channel_file = create_empty_channel(inputfile, img_dir)
    print('Empty channel is produced!')

    # Loop through file_list and add to the cube
    for file_index, filename in enumerate(file_list):
        # Adjust the replacement based on modified drop_indices
        if file_index in drop_indices.get(stokes, []):
            filename = empty_channel_file
            print(f"Replacing index {file_index} with empty channel for Stokes {stokes}")

        if not os.path.exists(filename):
            filename = empty_channel_file
            print(f"File not found at index {file_index}, using empty channel")

        with fits.open(filename) as hdulistCP:
            imgCP = hdulistCP[0].data
            if filename == empty_channel_file:
                imgCP[np.isnan(imgCP)] = 1e30
            img2cube = np.copy(imgCP[0, :, :, :])
            cube = np.append(cube, img2cube, axis=0)

        print(f"Added file {os.path.basename(filename)} to cube at index {file_index}")

    print(f"Cube completed for Stokes {stokes}")

    try:
        hdulist[0].data = cube
        hdulist.writeto(cubename, overwrite=True)
        print(f"Cube saved for Stokes {stokes} at {cubename}")
    except Exception as e:
        print(f"Error saving cube for {stokes}: {e}")

print("\nFinished creating all cubes.")
