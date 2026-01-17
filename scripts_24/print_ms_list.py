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

# === Find calibrated MS files ===
def find_calibrated_files(base_directory):
    calibrated_files = []
    if not os.path.exists(base_directory):
        return calibrated_files
    for subfolder in os.listdir(base_directory):
        sub_path = os.path.join(base_directory, subfolder)
        if os.path.isdir(sub_path) and subfolder.startswith('24A'):
            for file in os.listdir(sub_path):
                if file.endswith('_calibrated.ms'):
                    calibrated_files.append(os.path.join(sub_path, file))
    return calibrated_files

# === Print MS files for all mosaics ===
print('='*80)
print('MS FILES FOR ALL MOSAICS:')
print('='*80)

for mosaic_name in mosaic_names:
    base_directory = base_path + mosaic_name
    ms_file_list = find_calibrated_files(base_directory)

    print(f"\n[MOSAIC: {mosaic_name}]")
    if ms_file_list:
        for i, file in enumerate(ms_file_list):
            print(f"  [{i}] {file}")
    else:
        print(f"  No MS files found in {base_directory}")

print('\n' + '='*80)
