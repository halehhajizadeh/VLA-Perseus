import os
from casatasks import listobs
import matplotlib.pyplot as plt

# Define the base path where your MS files are located
base_path = "/data/new/data/"

# List to store MS files and their phase centers
ms_phase_centers = []

# Function to extract phase center using listobs
def get_phase_center(ms_file):
    output = listobs(ms_file, listfile=f'{ms_file}_listobs.txt', verbose=True)
    
    with open(f'{ms_file}_listobs.txt') as f:
        lines = f.readlines()
        for line in lines:
            if "Phase center" in line:
                ra_dec = line.split(":")[1].strip().split()
                ra, dec = ra_dec[0], ra_dec[1]
                return ra, dec

# Loop through the directories and find the MS files
for root, dirs, files in os.walk(base_path):
    for file in files:
        if file.endswith(".ms"):
            ms_file = os.path.join(root, file)
            phase_center = get_phase_center(ms_file)
            if phase_center:
                ms_phase_centers.append((ms_file, phase_center))

# Save the list of MS files and their phase centers
with open('ms_phase_centers.txt', 'w') as f:
    for ms_file, phase_center in ms_phase_centers:
        f.write(f"{ms_file}: RA = {phase_center[0]}, DEC = {phase_center[1]}\n")

import matplotlib.pyplot as plt

# Function to plot phase center of each MS
def plot_phase_center(ms_file, phase_center, fig_num):
    ra, dec = phase_center
    plt.figure(fig_num)
    plt.scatter(float(ra), float(dec), color='blue')
    plt.xlabel('RA (deg)')
    plt.ylabel('DEC (deg)')
    plt.title(f'Phase Center of {ms_file}')
    plt.savefig(f'phase_center_{fig_num}.png')
    plt.close()

# Loop through each MS and plot the phase center
for i, (ms_file, phase_center) in enumerate(ms_phase_centers):
    plot_phase_center(ms_file, phase_center, i)

# Function to plot all phase centers together
def plot_all_phase_centers(ms_phase_centers):
    plt.figure(figsize=(8, 6))
    
    for ms_file, phase_center in ms_phase_centers:
        ra, dec = phase_center
        plt.scatter(float(ra), float(dec), color='blue', label=ms_file)
    
    plt.xlabel('RA (deg)')
    plt.ylabel('DEC (deg)')
    plt.title('Phase Centers of All Measurement Sets')
    plt.savefig('all_phase_centers.png')
    plt.show()

# Call the function to plot all phase centers
plot_all_phase_centers(ms_phase_centers)
