import matplotlib
matplotlib.use('Agg')  # Use a non-interactive backend to avoid OpenGL issues
import matplotlib.pyplot as plt
import os
from casatools import msmetadata as msmdtool

# Ensure the phasecenter directory exists
output_dir = './phasecenter'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)  # Create directory if it doesn't exist

# Function to find directories and search for .ms files inside
def find_ms_file_in_directories(base_directory, startswith='24A-', endswith='.ms'):
    ms_files = []
    # Loop through the directories in the base directory
    for directory in os.listdir(base_directory):
        full_path = os.path.join(base_directory, directory)
        if os.path.isdir(full_path):  # Ensure it's a directory
            # Search for the .ms file inside the directory
            for file in os.listdir(full_path):
                if file.startswith(startswith) and file.endswith(endswith):
                    ms_files.append(os.path.join(full_path, file))  # Store the full path to the .ms file
    return ms_files

# Extract the phase center from the measurement set in J2000 format using msmetadata
def get_phase_center(ms_file):
    msmd = msmdtool()
    try:
        msmd.open(ms_file)
        ra_j2000 = msmd.phasecenter(0, unit='hms')['m0']['value']  # RA in J2000 (hours:min:sec)
        dec_j2000 = msmd.phasecenter(0, unit='dms')['m1']['value']  # DEC in J2000 (deg:arcmin:arcsec)
        msmd.close()
        return ra_j2000, dec_j2000
    except Exception as e:
        print(f"Error reading phase center from {ms_file}: {e}")
        return None

# Define working directory where your directories containing .ms files are located
working_directory = '../data/new/data'

# Debug: Print working directory
print(f"Looking for .ms files in directories inside: {working_directory}")

# Find all .ms files inside the directories
mslist = find_ms_file_in_directories(working_directory)

# Debug: Check if MS files were found
if not mslist:
    print("No .ms files found in the specified directories.")
else:
    print(f"Found {len(mslist)} .ms files.")

# Initialize lists for storing all phase centers
all_ra_deg = []
all_dec_deg = []
all_IDs = []

# Process each MS file, extract phase center, and generate plots
for ms_file in mslist:
    print(f"Processing {ms_file}...")

    # Get phase center (RA, Dec in J2000 format)
    phase_center = get_phase_center(ms_file)
    
    if phase_center is None:
        print(f"Skipping {ms_file} due to missing phase center.")
        continue  # Skip this MS file if phase center couldn't be read
    
    ra_j2000, dec_j2000 = phase_center
    print(f"Extracted phase center for {ms_file}: RA = {ra_j2000}, DEC = {dec_j2000}")
    all_ra_deg.append(ra_j2000)
    all_dec_deg.append(dec_j2000)
    ms_name = os.path.basename(ms_file)
    all_IDs.append(ms_name)

    # Plot individual MS phase centers
    plt.figure(figsize=(8, 6))
    plt.plot(float(ra_j2000), float(dec_j2000), 'bo')
    plt.xlabel('RA (J2000)', fontsize=12)
    plt.ylabel('DEC (J2000)', fontsize=12)
    plt.title(f'Phase Center of {ms_name}', fontsize=12)
    
    # Save individual plot for the MS
    plt.savefig(f'./phasecenter/{ms_name}_phase_center.png', dpi=150)
    plt.close()

# Check if we have valid phase centers to plot
if all_ra_deg:
    # Plot all phase centers together
    plt.figure(figsize=(10, 8))
    plt.plot([float(ra) for ra in all_ra_deg], [float(dec) for dec in all_dec_deg], 'bo')
    plt.xlabel('RA (J2000)', fontsize=12)
    plt.ylabel('DEC (J2000)', fontsize=12)
    plt.title('Phase Centers of All Measurement Sets (J2000)', fontsize=12)

    # Annotate all points with their IDs
    for i, ms_name in enumerate(all_IDs):
        plt.annotate(ms_name, (float(all_ra_deg[i]), float(all_dec_deg[i])), fontsize=8)

    # Save the combined plot of all phase centers
    plt.savefig('./phasecenter/all_phase_centers.png', dpi=150)
    plt.close()

    # Save phase center data to a file
    with open('./phasecenter/phase_centers_j2000.txt', 'w') as f:
        for ms_name, ra_j2000, dec_j2000 in zip(all_IDs, all_ra_deg, all_dec_deg):
            f.write(f"{ms_name}: RA (J2000) = {ra_j2000}, DEC (J2000) = {dec_j2000}\n")

    print("Phase centers (J2000) plotted and saved successfully.")
else:
    print("No phase centers found to plot.")
