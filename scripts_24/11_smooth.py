import os
import time
import sys
sys.path.append('.')

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
mosaic_name = '03:26:24.057_+30.35.58.881'
# mosaic_name = '03:29:12.973_+31.48.05.579'
# mosaic_name = '03:31:12.055_+29.47.58.916'
# mosaic_name = '03:39:12.060_+31.23.58.844'
# mosaic_name = '03:40:00.063_+32.23.58.799'
# mosaic_name = '03:42:00.057_+30.29.58.885'
# mosaic_name = '03:45:12.060_+31.41.58.831'
# mosaic_name = '03:45:36.064_+32.47.58.780'

concat_base = f'/lustre/aoc/observers/nm-12934/VLA-Perseus/data/new/data/concat/{mosaic_name}'

# === Run imsmooth for each SPW, channel, and Stokes ===
tic = time.time()

for stok in stokes:
    for s in spw:
        for channel in channels:
            print(f"\nSmoothing: Stokes {stok}, spw: {s}, channel: {channel} ...")

            input_dir = f"{concat_base}/Images/img/tclean"
            output_dir = f"{concat_base}/Images/img/smo"
            os.makedirs(output_dir, exist_ok=True)

            image_name = f"{input_dir}/spw{s}-{channel}-2.5arcsec-nit{nit}-{thresh}-{stok}.image"
            smo_image_name = f"{output_dir}/spw{s}-{channel}-2.5arcsec-nit{nit}-{thresh}-{stok}.image.smo"

            print(f"Input:  {image_name}")
            print(f"Output: {smo_image_name}")

            if not os.path.exists(image_name):
                print(f"WARNING: Image not found, skipping: {image_name}")
                continue

            imsmooth(imagename=image_name,
                     targetres=True,
                     major='20arcsec',
                     minor='20arcsec',
                     pa='0.0deg',
                     outfile=smo_image_name,
                     overwrite=True
                     )

toc = time.time()
print(f"\nFinished the smoothing process in {round((toc-tic)/60, 2)} minutes")
