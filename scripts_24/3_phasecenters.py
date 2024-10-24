import os
from casatasks import listobs
from casatools import msmetadata as msmdtool
import matplotlib.pyplot as plt

# Define the base path where your MS files are located
base_path = "/data/new/data/"

# List to store MS files and their phase centers
ms_phase_centers = []

# Function to extract phase center using msmetadata tool
def get_phase_center_from_ms(ms_file):
    msmd = msmdtool()
    try:
        msmd.open(ms_file)
        # Get the phase center of the first field (you can adjust the index if necessary)
        if msmd.nfields() > 0:
            phase_center = msmd.phasecenter(0)  # Use field index 0 (first field)
            ra = phase_center['m0']['value']  # RA value
            dec = phase_center['m1']['value']  # DEC value
            msmd.close()
            return ra, dec
        else:
            print(f"No fields found in {ms_file}")
            msmd.close()
            return None
    except Exception as e:
        print(f"Error accessing {ms_file}: {e}")
        return None

# Function to plot phase center of each MS
def plot_phase_center(ms_file, phase_center, fig_num):
    ra, dec = phase_center
    plt.figure(fig_num)
    plt.scatter(float(ra), float(dec), color='blue')
    plt.xlabel('RA (deg)')
    plt.ylabel('DEC (deg)')
    plt.title(f'Phase Center of {os.path.basename(ms_file)}')
    plt.savefig(f'phase_center_{fig_num}.png')
    plt.close()

# Function to plot all phase centers together
def plot_all_phase_centers(ms_phase_centers):
    plt.figure(figsize=(8, 6))
    
    for ms_file, phase_center in ms_phase_centers:
        ra, dec = phase_center
        plt.scatter(float(ra), float(dec), color='blue', label=os.path.basename(ms_file))
    
    plt.xlabel('RA (deg)')
    plt.ylabel('DEC (deg)')
    plt.title('Phase Centers of All Measurement Sets')
    plt.legend(loc='upper right')
    plt.savefig('all_phase_centers.png')
    plt.show()

# Main function to process all MS files
def process_all_ms_files(base_path):
    # Walk through the directories to find all MS files
    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file.endswith("_calibrated.ms"):  # Identify calibrated MS files
                ms_file = os.path.join(root, file)
                
                # Debugging print statement
                print(f"Processing {ms_file}...")
                
                # Get the phase center (RA, DEC)
                phase_center = get_phase_center_from_ms(ms_file)
                
                if phase_center is not None:
                    print(f"Phase Center for {ms_file}: RA = {phase_center[0]}, DEC = {phase_center[1]}")
                    ms_phase_centers.append((ms_file, phase_center))
                    
                    # Plot the phase center for this MS
                    plot_phase_center(ms_file, phase_center, len(ms_phase_centers))
                else:
                    print(f"Could not find phase center for {ms_file}")

    # Save the list of MS files and their phase centers
    if ms_phase_centers:
        with open('ms_phase_centers.txt', 'w') as f:
            for ms_file, phase_center in ms_phase_centers:
                f.write(f"{ms_file}: RA = {phase_center[0]}, DEC = {phase_center[1]}\n")

        # Plot all phase centers together
        plot_all_phase_centers(ms_phase_centers)
    else:
        print("No phase centers found in any measurement set.")

# Execute the function
process_all_ms_files(base_path)
