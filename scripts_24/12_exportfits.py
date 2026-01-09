import os
import time
import sys
sys.path.append('.')

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
    # 'Q',
    # 'U'
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

# === Run exportfits for each MS, SPW, and Stokes ===
tic = time.time()

for ms_path in ms_file_list:
    ms_name = os.path.basename(ms_path).replace('_calibrated.ms', '')

    for stok in stokes:
        for s in spw:
            print(f"\nExporting: Stokes {stok}, {ms_name}, spw: {s} ...")

            smo_dir = f"/lustre/aoc/observers/nm-12934/VLA-Perseus/data/new/data/concat/{mosaic_name}/Images/spw/{ms_name}/smo/spw{s}"
            fits_dir = f"/lustre/aoc/observers/nm-12934/VLA-Perseus/data/new/data/concat/{mosaic_name}/Images/spw/{ms_name}/fits/spw{s}"
            os.makedirs(fits_dir, exist_ok=True)

            smo_image_name = smo_dir + '/' + f"{ms_name}_Stokes{stok}_spw{s}-2.5arcsec-nit{nit}-awproject.image.tt0.smo"
            fits_image_name = fits_dir + '/' + f"{ms_name}_Stokes{stok}_spw{s}-2.5arcsec-nit{nit}-awproject.image.tt0.smo.fits"

            print(f"Input:  {smo_image_name}")
            print(f"Output: {fits_image_name}")

            if not os.path.exists(smo_image_name):
                print(f"WARNING: Smoothed image not found, skipping: {smo_image_name}")
                continue

            exportfits(imagename=smo_image_name,
                       fitsimage=fits_image_name,
                       overwrite=True
                       )

toc = time.time()
print(f"\nFinished the exporting process in {round((toc-tic)/60, 2)} minutes")
