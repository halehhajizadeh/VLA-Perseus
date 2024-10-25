import matplotlib
matplotlib.use('Agg')  # Force matplotlib to use a non-interactive backend
import matplotlib.pyplot as plt
import os
from casatools import msmetadata as msmdtool  # CASA tool for metadata access

# Ensure the phasecenter directory exists
output_dir = './phasecenter'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)  # Create directory if it doesn't exist

# Function to find MS folders in the directory
def find_ms_folder(directory, startswith='24A-', endswith='_calibrated.ms'):
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

# Define working directory where your MS files are located
working_directory = '/data/new/data'

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
    plt.plot(ra_deg, dec_deg, 'bo')
    plt.xlabel('RA (deg)', fontsize=12)
    plt.ylabel('DEC (deg)', fontsize=12)
    plt.title(f'Phase Center of {ms_name}', fontsize=12)
    
    # Save individual plot for the MS
    plt.savefig(f'./phasecenter/{ms_name}_phase_center.png', dpi=150)
    plt.close()

# Plot all phase centers together
plt.figure(figsize=(10, 8))
plt.plot(all_ra_deg, all_dec_deg, 'bo')
plt.xlabel('RA (deg)', fontsize=12)
plt.ylabel('DEC (deg)', fontsize=12)
plt.title('Phase Centers of All Measurement Sets', fontsize=12)

# Annotate all points with their IDs
for i, ms_name in enumerate(all_IDs):
    plt.annotate(ms_name, (all_ra_deg[i], all_dec_deg[i]), fontsize=8)

# Save the combined plot of all phase centers
plt.savefig('./phasecenter/all_phase_centers.png', dpi=150)
plt.close()

# Save phase center data to a file
with open('./phasecenter/phase_centers.txt', 'w') as f:
    for ms_name, ra_deg, dec_deg in zip(all_IDs, all_ra_deg, all_dec_deg):
        f.write(f"{ms_name}: RA = {ra_deg}, DEC = {dec_deg}\n")

print("Phase centers plotted and saved successfully.")
