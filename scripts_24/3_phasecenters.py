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

# Function to extract phase center for each field in the mosaic
def get_mosaic_phase_centers(ms_file):
    msmd = msmdtool()
    phase_centers = []
    try:
        msmd.open(ms_file)
        fields = msmd.fieldsforname('PER_FIELD_*')  # Get all fields matching 'PER_FIELD_*'
        for field_id in fields:
            ra_deg = msmd.phasecenter(field_id)['m0']['value']
            dec_deg = msmd.phasecenter(field_id)['m1']['value']
            phase_centers.append((ra_deg, dec_deg, msmd.fieldnames()[field_id]))
        msmd.close()
    except Exception as e:
        print(f"Error reading phase centers from {ms_file}: {e}")
    return phase_centers

# Define working directory
working_directory = '../data/new/data'
mslist = find_ms_folder(working_directory)

# Check if any .ms files are found
if not mslist:
    print("No .ms files found.")
else:
    print(f"Found {len(mslist)} .ms files.")

# Initialize lists for storing all phase centers
all_ra_deg = []
all_dec_deg = []
all_IDs = []

# Process each MS file and extract phase centers for each field
for ms_file in mslist:
    print(f"Processing {ms_file}...")
    phase_centers = get_mosaic_phase_centers(ms_file)
    
    for ra_deg, dec_deg, field_name in phase_centers:
        all_ra_deg.append(ra_deg)
        all_dec_deg.append(dec_deg)
        all_IDs.append(field_name)

# Combined plot for all phase centers in the mosaic
if all_ra_deg:
    plt.figure(figsize=(10, 8))
    plt.plot(all_ra_deg, all_dec_deg, 'bo')  # 'bo' indicates blue dots
    plt.xlabel(r'RA (deg)', fontsize=15)
    plt.ylabel(r'DEC (deg)', fontsize=15)
    plt.title('Phase Centers of Mosaic Fields (J2000)', fontsize=15)

    # Annotate all points with their IDs if desired
    for i, field_name in enumerate(all_IDs):
        plt.annotate(field_name, (all_ra_deg[i], all_dec_deg[i]), fontsize=8)

    # Save the combined plot of all phase centers
    plt.savefig('./phasecenter/mosaic_phase_centers.png', dpi=150)
    plt.close()

    print("Mosaic phase centers plotted and saved successfully.")
else:
    print("No phase centers found to plot.")
