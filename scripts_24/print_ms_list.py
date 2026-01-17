import os
import sys
sys.path.append('.')

mosaic_name = '03:29:12.973_+31.48.05.579'

base_directory = '/lustre/aoc/observers/nm-12934/VLA-Perseus/data/new/data/' + mosaic_name

# === Find calibrated MS files ===
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
print('='*80)
print('Available MS files:')
print('='*80)
for i, file in enumerate(ms_file_list):
    print(f"[{i}] {file}")
print('='*80)
