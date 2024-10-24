import sys
import matplotlib.pyplot as plt
import numpy as np
import os
from casatools import msmetadata as msmdtool

# Disable LaTeX rendering for Matplotlib to avoid errors
from matplotlib import rc
rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
rc('text', usetex=False)  # Set usetex to False

# Define working directory where your MS files are located
working_directory = '/data/new/data'

# Function to find MS folders in the directory
def find_ms_folder(directory, startswith='24A-', endswith='.ms'):
    folders_list = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.startswith(startswith) and file.endswith(endswith):
                folders_list.append(os.path.join(root, file))                
    return folders_list

# Extract the phase center from the measurement set using msmetadata
def get_phase_center(ms_file):
    msmd = msmdtool()
    try:
        msmd.open(ms_file)
        ra_deg = msmd.phasecenter(0)['m0']['value']  # RA in degrees
        dec_deg = msmd.phasecenter(0)['m1']['value']  # DEC in degrees
        msmd.close()
        return ra_deg, dec_deg
    except Exception as e:
        print(f"Error reading phase center from {ms_file}: {e}")
        return None

# Find all MS files
mslist = find_ms_folder(working_directory)

# Initialize lists for storing all phase centers
all_ra_deg = []
all_dec_deg = []
all_IDs = []

# Process each MS file, extract phase center, and generate plots
for ms_folder in mslist:
    print(f"Processing {ms_folder}...")

    # Get phase center (RA, Dec in degrees)
    phase_center = get_phase_center(ms_folder)
    
    if phase_center is None:
        continue  # Skip this MS file if phase center couldn't be read
    
    ra_deg, dec_deg = phase_center
    all_ra_deg.append(ra_deg)
    all_dec_deg.append(dec_deg)
    ms_name = os.path.basename(ms_folder)
    all_IDs.append(ms_name)

    # Plot individual MS phase centers
    plt.figure(figsize=(8, 6))
    plt.plot(ra_deg, dec_deg, 'b.')
    plt.xlabel('RA (deg)', fontsize=15)
    plt.ylabel('DEC (deg)', fontsize=15)
    plt.title(f'Phase Center of {ms_name}', fontsize=15)
    plt.tick_params(axis='x', labelsize=14)
    plt.tick_params(axis='y', labelsize=14)
    
    # Save individual plot for the MS
    plt.savefig(f'./phasecenter/{ms_name}_phase_center.png')
    plt.close()

# Plot all phase centers together
plt.figure(figsize=(10, 8))
plt.plot(all_ra_deg, all_dec_deg, 'b.')
plt.xlabel('RA (deg)', fontsize=15)
plt.ylabel('DEC (deg)', fontsize=15)
plt.title('Phase Centers of All Measurement Sets', fontsize=15)
plt.tick_params(axis='x', labelsize=14)
plt.tick_params(axis='y', labelsize=14)

# Annotate all points with their IDs
for i, ms_name in enumerate(all_IDs):
    plt.annotate(ms_name, (all_ra_deg[i], all_dec_deg[i]))

# Save the combined plot of all phase centers
plt.savefig('./phasecenter/all_phase_centers.png')
plt.show()

# Save phase center data to a file
with open('./phasecenter/phase_centers.txt', 'w') as f:
    for ms_name, ra_deg, dec_deg in zip(all_IDs, all_ra_deg, all_dec_deg):
        f.write(f"{ms_name}: RA = {ra_deg}, DEC = {dec_deg}\n")
