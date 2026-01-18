import os
import sys
sys.path.append('.')

# === All mosaic names ===
mosaic_names = [
    '03:26:24.057_+30.35.58.881',
    '03:29:12.973_+31.48.05.579',
    '03:31:12.055_+29.47.58.916',
    '03:39:12.060_+31.23.58.844',
    '03:40:00.063_+32.23.58.799',
    '03:42:00.057_+30.29.58.885',
    '03:45:12.060_+31.41.58.831',
    '03:45:36.064_+32.47.58.780'
]

base_path = '/lustre/aoc/observers/nm-12934/VLA-Perseus/data/new/data/'

# === Find 24A directories ===
def find_24a_directories(base_directory):
    directories = []
    if not os.path.exists(base_directory):
        return directories
    for subfolder in os.listdir(base_directory):
        if subfolder.startswith('24A'):
            directories.append(subfolder)
    return directories

# === Print 24A directories for all mosaics ===
print('='*80)
print('24A DIRECTORIES FOR ALL MOSAICS:')
print('='*80)

for mosaic_name in mosaic_names:
    base_directory = base_path + mosaic_name
    dir_list = find_24a_directories(base_directory)

    print(f"\n[MOSAIC: {mosaic_name}]")
    if dir_list:
        for i, directory in enumerate(dir_list):
            print(f"  [{i}] {directory}")
    else:
        print(f"  No 24A directories found")

print('\n' + '='*80)
