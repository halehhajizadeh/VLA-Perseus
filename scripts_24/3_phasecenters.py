import os
import matplotlib
matplotlib.use('Agg')  # Use a non-interactive backend to avoid OpenGL issues
import matplotlib.pyplot as plt
from casatools import msmetadata as msmdtool
import math

# Define the directory for output files and plots
output_dir = './phasecenter'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Function to find .ms files in a specified directory structure
def find_ms_folder(directory, startswith='24A-', endswith='_calibrated.ms'):
    ms_files = []
    for file in os.listdir(directory):
        full_path = os.path.join(directory, file)
        if os.path.isdir(full_path):
            for inner_file in os.listdir(full_path):
                if inner_file.startswith(startswith) and inner_file.endswith(endswith):
                    ms_files.append(os.path.join(full_path, inner_file))
    return ms_files

# Function to convert RA in degrees to hours:minutes:seconds (J2000)
def degrees_to_hms(ra_deg):
    total_seconds = ra_deg * 240  # 1 degree = 240 seconds (15 degrees per hour)
    hours = int(total_seconds // 3600)
    minutes = int((total_seconds % 3600) // 60)
    seconds = total_seconds % 60
    return f"{hours:02d}:{minutes:02d}:{seconds:06.3f}"

# Function to convert Dec in degrees to degrees.arcminutes.arcseconds (J2000)
def degrees_to_dms(dec_deg):
    sign = "-" if dec_deg < 0 else "+"
    dec_deg = abs(dec_deg)
    degrees = int(dec_deg)
    arcminutes = int((dec_deg - degrees) * 60)
    arcseconds = (dec_deg - degrees - arcminutes / 60) * 3600
    return f"{sign}{degrees:02d}.{arcminutes:02d}.{arcseconds:06.3f}"

# Function to convert RA in HH:MM:SS format to degrees
def hms_to_degrees(ra_hms):
    h, m, s = [float(x) for x in ra_hms.split(":")]
    return (h + m / 60 + s / 3600) * 15

# Function to convert Dec in DD.MM.SS.sss format to degrees
def dms_to_degrees(dec_dms):
    try:
        # Split only on the first two dots for degrees and arcminutes
        parts = dec_dms.split('.')
        if len(parts) < 3:
            raise ValueError(f"Invalid Dec format: {dec_dms}")
        
        # Handle degrees, arcminutes, and arcseconds
        d = float(parts[0])  # Degrees
        m = float(parts[1])  # Arcminutes
        s = float('.'.join(parts[2:]))  # Combine remaining parts as arcseconds
        
        sign = -1 if d < 0 else 1  # Determine the sign
        return sign * (abs(d) + m / 60 + s / 3600)
    except Exception as e:
        raise ValueError(f"Error converting Dec '{dec_dms}' to degrees: {e}")


def get_per_field_phase_centers(ms_file):
    msmd = msmdtool()
    phase_centers = []
    try:
        msmd.open(ms_file)
        for field_id in range(msmd.nfields()):
            field_name = msmd.fieldnames()[field_id]
            if field_name.startswith("PER_FIELD_"):
                # Fetch RA and Dec directly in degrees from the FIELD table
                ra_deg = msmd.phasecenter(field_id)['m0']['value'] * (180.0 / math.pi)  # Convert from radians to degrees
                dec_deg = msmd.phasecenter(field_id)['m1']['value'] * (180.0 / math.pi)  # Convert from radians to degrees

                # Convert RA degrees to HH:MM:SS format
                ra_hms = degrees_to_hms(ra_deg)

                # Convert Dec degrees to ±DD.MM.SS format
                dec_dms = degrees_to_dms(dec_deg)

                phase_centers.append((field_id, ra_hms, dec_dms))
        msmd.close()
    except Exception as e:
        print(f"Error reading phase centers from {ms_file}: {e}")
    return phase_centers

# Define the working directory containing measurement sets
working_directory = '../data/new/data'
mslist = find_ms_folder(working_directory)

# Check if any .ms files are found
if not mslist:
    print("No .ms files found.")
else:
    print(f"Found {len(mslist)} .ms files.")

# Initialize lists for combined plotting
all_ra_deg = []
all_dec_deg = []
all_IDs = []

# Process each measurement set
with open('./phasecenter/measurement_sets_phase_centers.txt', 'w') as summary_file:
    for ms_file in mslist:
        # Get the base name and remove "_calibrated.ms"
        ms_name = os.path.basename(ms_file).replace("_calibrated.ms", "")
        print(f"Processing {ms_name}...")

        # Extract phase centers for each field matching "PER_FIELD_*"
        phase_centers = get_per_field_phase_centers(ms_file)

        # Check if phase centers were found
        if not phase_centers:
            print(f"No phase centers found for {ms_name}, skipping.")
            continue

        # Write field centers to a separate file for each measurement set
        phase_center_filename = f'./phasecenter/{ms_name}_field_centers.txt'
        with open(phase_center_filename, 'w') as f:
            for field_id, ra, dec in phase_centers:
                f.write(f"{field_id}\t{ra}\t{dec}\n")

        # Plot phase centers for individual measurement set
        ra_deg_list = [hms_to_degrees(ra) for _, ra, _ in phase_centers]
        dec_deg_list = [dms_to_degrees(dec) for _, _, dec in phase_centers]
        plt.figure(figsize=(8, 6))
        plt.plot(ra_deg_list, dec_deg_list, 'bo')
        plt.xlabel('RA (deg)', fontsize=15)
        plt.ylabel('DEC (deg)', fontsize=15)
        plt.title(f'Phase Centers of Fields in {ms_name}', fontsize=15)

        # Annotate each field
        for i, field_id in enumerate([field_id for field_id, _, _ in phase_centers]):
            plt.annotate(field_id, (ra_deg_list[i], dec_deg_list[i]), fontsize=8)

        # Save plot for this measurement set
        plt.savefig(f'./phasecenter/{ms_name}_field_centers_plot.png', dpi=150)
        plt.close()

        # Summarize the main phase center for this measurement set in degrees
        main_ra_deg = sum(ra_deg_list) / len(ra_deg_list)
        main_dec_deg = sum(dec_deg_list) / len(dec_deg_list)
        main_ra_j2000 = degrees_to_hms(main_ra_deg)
        main_dec_j2000 = degrees_to_dms(main_dec_deg)

        # Append for combined plotting
        all_ra_deg.extend(ra_deg_list)
        all_dec_deg.extend(dec_deg_list)
        all_IDs.extend([field_id for field_id, _, _ in phase_centers])

        # Write to summary file with modified ms_name
        summary_file.write(f"{ms_name}: J2000 {main_ra_j2000} {main_dec_j2000}\n")

# Plot all phase centers together (combined plot)
if all_ra_deg:
    plt.figure(figsize=(10, 8))
    plt.plot(all_ra_deg, all_dec_deg, 'bo')
    plt.xlabel(r'RA (deg)', fontsize=15)
    plt.ylabel(r'DEC (deg)', fontsize=15)
    plt.title('Combined Phase Centers of All Measurement Sets (J2000)', fontsize=15)

    # Annotate all points with their field IDs
    for i, field_id in enumerate(all_IDs):
        plt.annotate(field_id, (all_ra_deg[i], all_dec_deg[i]), fontsize=6)

    # Save the combined plot
    plt.savefig('./phasecenter/combined_phase_centers.png', dpi=150)
    plt.close()

    print("All phase centers plotted and saved successfully.")
else:
    print("No phase centers found to plot.")
