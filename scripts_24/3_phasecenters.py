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

# Function to convert RA in degrees to hours:minutes:seconds (J2000)
def degrees_to_hms(ra_deg):
    hours = int(ra_deg // 15)
    minutes = int((ra_deg % 15) * 4)
    seconds = (((ra_deg % 15) * 4) % 1) * 60
    return f"{hours:02d}:{minutes:02d}:{seconds:06.3f}"

# Function to convert Dec in degrees to degrees:arcminutes:arcseconds (J2000)
def degrees_to_dms(dec_deg):
    degrees = int(dec_deg)
    arcminutes = int(abs((dec_deg - degrees) * 60))
    arcseconds = abs(((dec_deg - degrees) * 60 - arcminutes) * 60)
    return f"{degrees:+03d}:{arcminutes:02d}:{arcseconds:06.3f}"

# Function to convert RA/Dec from J2000 (HMS/DMS) back to degrees
def hms_to_degrees(ra_hms):
    h, m, s = [float(x) for x in ra_hms.split(":")]
    return (h + m / 60 + s / 3600) * 15

def dms_to_degrees(dec_dms):
    d, m, s = [float(x) for x in dec_dms.split(":")]
    sign = -1 if d < 0 else 1
    return sign * (abs(d) + m / 60 + s / 3600)

# Extract the phase center from the measurement set using msmetadata
def get_phase_center(ms_file):
    msmd = msmdtool()
    try:
        msmd.open(ms_file)
        ra_deg = msmd.phasecenter(0)['m0']['value']  # RA in degrees
        dec_deg = msmd.phasecenter(0)['m1']['value']  # DEC in degrees
        msmd.close()
        
        ra_j2000 = degrees_to_hms(ra_deg)  # Convert RA from degrees to J2000 format
        dec_j2000 = degrees_to_dms(dec_deg)  # Convert DEC from degrees to J2000 format
        
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
    all_ra_deg.append(hms_to_degrees(ra_j2000))  # Convert back to degrees for plotting
    all_dec_deg.append(dms_to_degrees(dec_j2000))  # Convert back to degrees for plotting
    ms_name = os.path.basename(ms_file)
    all_IDs.append(ms_name)

    # Plot individual MS phase centers
    plt.figure(figsize=(8, 6))
    plt.plot(all_ra_deg[-1], all_dec_deg[-1], 'bo')
    plt.xlabel('RA (deg)', fontsize=12)
    plt.ylabel('DEC (deg)', fontsize=12)
    plt.title(f'Phase Center of {ms_name}', fontsize=12)
    
    # Save individual plot for the MS
    plt.savefig(f'./phasecenter/{ms_name}_phase_center.png', dpi=150)
    plt.close()

# Check if we have valid phase centers to plot
if all_ra_deg:
    # Plot all phase centers together
    plt.figure(figsize=(10, 8))
    plt.plot(all_ra_deg, all_dec_deg, 'bo')
    plt.xlabel('RA (deg)', fontsize=12)
    plt.ylabel('DEC (deg)', fontsize=12)
    plt.title('Phase Centers of All Measurement Sets (J2000)', fontsize=12)

    # Annotate all points with their IDs
    for i, ms_name in enumerate(all_IDs):
        plt.annotate(ms_name, (all_ra_deg[i], all_dec_deg[i]), fontsize=8)

    # Save the combined plot of all phase centers
    plt.savefig('./phasecenter/all_phase_centers.png', dpi=150)
    plt.close()

    # Save phase center data to a file in the requested format
    with open('./phasecenter/phase_centers_j2000.txt', 'w') as f:
        for ms_name, ra_j2000, dec_j2000 in zip(all_IDs, all_ra_deg, all_dec_deg):
            # Format: "J2000 00:00:00.000 +00.00.00.000"
            formatted_ra = ra_j2000.replace(":", ".")
            formatted_dec = dec_j2000.replace(":", ".")
            f.write(f"{ms_name}: J2000 {formatted_ra} {formatted_dec}\n")

    print("Phase centers (J2000) plotted and saved successfully.")
else:
    print("No phase centers found to plot.")
