import sys
sys.path.append('.')
import numpy as np
import os

# === Parameters ===
thresh = '9e-5'
nit = 4000
spw = [
    2,
    3,
    4,
    5,
    6,
    8,
    15,
    16,
    17
    ]

stokes = [
    'I',
    'Q',
    'U'
]

channels = [
    '00~07',
    '08~15',
    '16~23',
    '24~31',
    '32~39',
    '40~47',
    '48~55',
    '56~63'
]

# === Choose ONE mosaic name to activate ===
# mosaic_name = '03:26:24.057_+30.35.58.881'
mosaic_name = '03:29:12.973_+31.48.05.579'
# mosaic_name = '03:31:12.055_+29.47.58.916'
# mosaic_name = '03:39:12.060_+31.23.58.844'
# mosaic_name = '03:40:00.063_+32.23.58.799'
# mosaic_name = '03:42:00.057_+30.29.58.885'
# mosaic_name = '03:45:12.060_+31.41.58.831'
# mosaic_name = '03:45:36.064_+32.47.58.780'

concat_base = f'/lustre/aoc/observers/nm-12934/VLA-Perseus/data/new/data/concat/{mosaic_name}'
fits_dir = f"{concat_base}/Images/img/fits"

# === Build image list for each SPW, channel, and Stokes ===
def build_image_list(stok):
    files_list = []
    for s in spw:
        for channel in channels:
            file_name = f"{fits_dir}/spw{s}-{channel}-2.5arcsec-nit{nit}-{thresh}-{stok}.image.smo.fits"

            if os.path.exists(file_name):
                files_list.append(file_name)
            else:
                files_list.append(f"{concat_base}/Images/img/empty_channel.fits")
    return files_list

# === Remove empty channels from the beginning of the list ===
def remove_initial_empty_channels(files_list):
    non_empty_start = 0
    for file_name in files_list:
        if "empty_channel.fits" not in file_name:
            break
        non_empty_start += 1
    return files_list[non_empty_start:]

# === Create output directory for image lists ===
list_output_dir = f"{concat_base}/Images/img"
os.makedirs(list_output_dir, exist_ok=True)

# === Main loop to process each Stokes parameter ===
for stok in stokes:
    files_list = build_image_list(stok)
    non_empty_files_list = remove_initial_empty_channels(files_list)

    output_file = os.path.join(list_output_dir, f"Stokes{stok}.txt")
    np.savetxt(output_file, non_empty_files_list, fmt='%s')
    print(f"File list for Stokes {stok} saved with {len(non_empty_files_list)} entries.")
    print(f"  -> {output_file}")

print("\nFinished creating image lists.")
