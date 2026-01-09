import sys
sys.path.append('.')
import numpy as np
import os

# === Parameters ===
thresh = '6e-5'
nit = 5000
spw = [
    # 2,
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

# === Choose ONE mosaic name to activate ===
mosaic_name = '03:26:24.057_+30.35.58.881'
# mosaic_name = '03:29:12.973_+31.48.05.579'
# mosaic_name = '03:31:12.055_+29.47.58.916'
# mosaic_name = '03:39:12.060_+31.23.58.844'
# mosaic_name = '03:40:00.063_+32.23.58.799'
# mosaic_name = '03:42:00.057_+30.29.58.885'
# mosaic_name = '03:45:12.060_+31.41.58.831'
# mosaic_name = '03:45:36.064_+32.47.58.780'

base_directory = '/lustre/aoc/observers/nm-12934/VLA-Perseus/data/new/data/' + mosaic_name
concat_base = f'/lustre/aoc/observers/nm-12934/VLA-Perseus/data/new/data/concat/{mosaic_name}'

# === Find calibrated MS files to get MS names ===
def find_calibrated_files(base_directory):
    calibrated_files = []
    for subfolder in os.listdir(base_directory):
        sub_path = os.path.join(base_directory, subfolder)
        if os.path.isdir(sub_path) and subfolder.startswith('24A'):
            for file in os.listdir(sub_path):
                if file.endswith('_calibrated.ms'):
                    calibrated_files.append(os.path.join(sub_path, file))
    return calibrated_files

ms_file_list = find_calibrated_files(base_directory)

# === Print MS file list ===
print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
for file in ms_file_list:
    print(file)
print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')

# === Build image list for each MS, SPW, and Stokes ===
def build_image_list(stok, ms_name):
    files_list = []
    for s in spw:
        fits_dir = f"{concat_base}/Images/spw/{ms_name}/fits/spw{s}"
        file_name = f"{fits_dir}/{ms_name}_Stokes{stok}_spw{s}-2.5arcsec-nit{nit}-awproject.image.tt0.smo.fits"

        if os.path.exists(file_name):
            files_list.append(file_name)
        else:
            files_list.append(f"{concat_base}/empty_channel.fits")
    return files_list

# === Remove empty channels from the beginning of the list ===
def remove_initial_empty_channels(files_list):
    non_empty_start = 0
    for file_name in files_list:
        if "empty_channel.fits" not in file_name:
            break
        non_empty_start += 1
    return files_list[non_empty_start:]

# === Main loop to process each MS and Stokes parameter ===
for ms_path in ms_file_list:
    ms_name = os.path.basename(ms_path).replace('_calibrated.ms', '')

    # Create output directory for image lists
    list_output_dir = f"{concat_base}/Images/spw/{ms_name}/lists"
    os.makedirs(list_output_dir, exist_ok=True)

    for stok in stokes:
        files_list = build_image_list(stok, ms_name)
        non_empty_files_list = remove_initial_empty_channels(files_list)

        output_file = os.path.join(list_output_dir, f"Stokes{stok}.txt")
        np.savetxt(output_file, non_empty_files_list, fmt='%s')
        print(f"{ms_name}: File list for Stokes {stok} saved with {len(non_empty_files_list)} entries.")
        print(f"  -> {output_file}")

print("\nFinished creating image lists.")
