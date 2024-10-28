import sys
sys.path.append('.')
import matplotlib
matplotlib.use('Agg')  # Use a non-interactive backend to avoid OpenGL issues
import matplotlib.pyplot as plt
import os
from casatools import msmetadata as msmdtool

# Define the directory for phase center plots
output_dir = './phasecenter'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Function to locate .ms files in a specified directory structure
def find_ms_folder(directory, startswith='24A-', endswith='.ms'):
    ms_files = []
    for file in os.listdir(directory):
        full_path = os.path.join(directory, file)
        if os.path.isdir(full_path):  # Check if it's a directory
            for inner_file in os.listdir(full_path):
                if inner_file.startswith(startswith) and inner_file.endswith(endswith):
                    ms_files.append(os.path.join(full_path, inner_file))
    return ms_files

# Functions for RA and Dec conversions
def degrees_to_hms(ra_deg):
    hours = int(ra_deg // 15)
    minutes = int((ra_deg % 15) * 4)
    seconds = (((ra_deg % 15) * 4) % 1) * 60
    return f"{hours:02d}:{minutes:02d}:{seconds:06.3f}"

def degrees_to_dms(dec_deg):
    degrees = int(dec_deg)
    arcminutes = int(abs((dec_deg - degrees) * 60))
    arcseconds = abs(((dec_deg - degrees) * 60 - arcminutes) * 60)
    return f"{degrees:+03d}:{arcminutes:02d}:{arcseconds:06.3f}"

def hms_to_degrees(ra_hms):
    h, m, s = [float(x) for x in ra_hms.split(":")]
    return (h + m / 60 + s / 3600) * 15

def dms_to_degrees(dec_dms):
    d, m, s = [float(x) for x in dec_dms.split(":")]
    sign = -1 if d < 0 else 1
    return sign * (abs(d) + m / 60 + s / 3600)

# Extract the phase center from the measurement set
def get_phase_center(ms_file):
    msmd = msmdtool()
    try:
        msmd.open(ms_file)
        ra_deg = msmd.phasecenter(0)['m0']['value']
        dec_deg = msmd.phasecenter(0)['m1']['value']
        msmd.close()
        
        ra_j2000 = degrees_to_hms(ra_deg)
        dec_j2000 = degrees_to_dms(dec_deg)
        return ra_j2000, dec_j2000
    except Exception as e:
        print(f"Error reading phase center from {ms_file}: {e}")
        return None

# Define working directory
working_directory = '../data/new/data'
mslist = find_ms_folder(working_directory)

if not mslist:
    print("No .ms files found.")
else:
    print(f"Found {len(mslist)} .ms files.")

all_ra_deg, all_dec_deg, all_IDs = [], [], []

for ms_file in mslist:
    print(f"Processing {ms_file}...")
    phase_center = get_phase_center(ms_file)
    
    if phase_center is None:
        print(f"Skipping {ms_file} due to missing phase center.")
        continue
    
    ra_j2000, dec_j2000 = phase_center
    all_ra_deg.append(hms_to_degrees(ra_j2000))
    all_dec_deg.append(dms_to_degrees(dec_j2000))
    ms_name = os.path.basename(ms_file)
    all_IDs.append(ms_name)
    
    # Individual MS phase center plot
    plt.figure(figsize=(8, 6))
    plt.plot(all_ra_deg[-1], all_dec_deg[-1], 'bo')
    plt.xlabel(r'RA (deg)', fontsize=15)
    plt.ylabel(r'DEC (deg)', fontsize=15)
    plt.title(f'Phase Center of {ms_name}', fontsize=15)
    plt.annotate(ms_name, (all_ra_deg[-1], all_dec_deg[-1]), fontsize=8)
    plt.savefig(f'./phasecenter/{ms_name}_phase_center.png', dpi=150)
    plt.close()

# Combined plot for all MS phase centers
if all_ra_deg:
    plt.figure(figsize=(10, 8))
    plt.plot(all_ra_deg, all_dec_deg, 'bo')
    plt.xlabel(r'RA (deg)', fontsize=15)
    plt.ylabel(r'DEC (deg)', fontsize=15)
    plt.title('Phase Centers of All Measurement Sets (J2000)', fontsize=15)

    for i, ms_name in enumerate(all_IDs):
        plt.annotate(ms_name, (all_ra_deg[i], all_dec_deg[i]), fontsize=8)

    plt.savefig('./phasecenter/all_phase_centers.png', dpi=150)
    plt.close()

    # Save phase center data in the requested format
    with open('./phasecenter/phase_centers_j2000.txt', 'w') as f:
        for ms_name, ra_j2000, dec_j2000 in zip(all_IDs, all_ra_deg, all_dec_deg):
            formatted_ra = ra_j2000.replace(":", ".")
            formatted_dec = dec_j2000.replace(":", ".")
            f.write(f"{ms_name}: J2000 {formatted_ra} {formatted_dec}\n")

    print("Phase centers (J2000) plotted and saved successfully.")
else:
    print("No phase centers found to plot.")
