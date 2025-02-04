import os
from glob import glob
import shutil

# Define your base path
base_path = "../data/new/data/"

def load_phase_centers(phase_center_file):
    phase_centers = {}
    try:
        with open(phase_center_file, 'r') as file:
            for line in file:
                # Debug: Print each line being read
                print(f"Reading line: {line.strip()}")

                # Check if the line contains a colon
                if ":" not in line:
                    print(f"Skipping malformed line (no colon): {line.strip()}")
                    continue

                # Split line into ms_name and phasecenter
                parts = line.strip().split(":", 1)  # Split only at the first colon
                if len(parts) != 2:
                    print(f"Skipping malformed line (invalid format): {line.strip()}")
                    continue

                ms_name = parts[0].strip()  # Extract and clean ms_name
                phasecenter = parts[1].strip()  # Extract and clean phasecenter

                # Debug: Print the parsed key-value pair
                print(f"Parsed: {ms_name} -> {phasecenter}")

                phase_centers[ms_name] = phasecenter

        print(f"Loaded phase centers: {phase_centers}")  # Debugging
    except Exception as e:
        print(f"Error reading phase centers file: {e}")
    return phase_centers


# Define the common parameters for tclean
def run_tclean(ms_file, img_filename, mosaic_name, phasecenter):
    thresh = '1e-4'
    pblim = -0.001
    nit = 6000

    # Delete all files and directories matching imagename.*
    for item in glob(img_filename + ".*"):
        if os.path.isfile(item):
            print(f"Deleting existing file: {item}")
            os.remove(item)
        elif os.path.isdir(item):
            print(f"Deleting existing directory: {item}")
            shutil.rmtree(item)

    # Run tclean with specified parameters
    tclean(
        vis=ms_file,
        field="PER_FIELD_*",
        timerange="",
        spw="",
        uvrange="",
        antenna="",
        observation="",
        intent="",
        datacolumn="corrected",
        imagename=img_filename,
        imsize=[4096],
        cell="2.5arcsec",
        phasecenter=str(phasecenter),  # Pass the phasecenter dynamically
        stokes='I',
        specmode="mfs",
        gridder="awproject",
        mosweight=True,
        # savemodel='',
        cfcache=f'/dev/shm/{mosaic_name}.cf',
        pblimit=pblim,
        deconvolver="mtmfs",
        pbcor=True,
        weighting="briggs",
        robust=0.5,
        niter=nit,
        gain=0.1,
        # nsigma=3,
        threshold=thresh,
        cycleniter=200,
        # psfcutoff=0.5,
        cyclefactor=1,
        parallel=True,
        # psterm=True,
        nterms=2,
        rotatepastep=5.0,
        interactive=False
    )

def process_all_ms_files(base_path, phase_centers):
    # Find all subdirectories inside base_path
    dirs = glob(os.path.join(base_path, "*/"))
    
    for directory in dirs:
        # Find the .ms file ending with '_calibrated.ms' in each directory
        ms_files = glob(os.path.join(directory, "*_calibrated.ms"))
        
        if ms_files:
            ms_file = ms_files[0]  # Assuming only one .ms file in each directory
            img_filename = os.path.join(directory, "newtest9")  # Define a unique image name
            mosaic_name = os.path.basename(directory).split('.')[0]  # Generate mosaic name from directory name
            
            # Extract and normalize the ms_name
            ms_name = os.path.basename(ms_file).replace("_calibrated.ms", "").strip()
            print(f"Processing ms_file: {ms_name}")
            
            # Match the phase center using the saved phase center file
            phasecenter = phase_centers.get(ms_name, "")
            if not phasecenter:
                print(f"Warning: No phase center found for {ms_name}. Skipping...")
                continue

            print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")    
            print(f"ms_name: {ms_name}")
            print(f"Phase Center Keys: {list(phase_centers.keys())}")
            print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")

            
            # Run tclean with the appropriate phase center
            print(f"Running tclean on {ms_file} with phase center: {phasecenter}")
            run_tclean(ms_file, img_filename, mosaic_name, phasecenter)

# Main execution
phase_center_file = './phasecenter/measurement_sets_phase_centers.txt'  # Path to saved phase centers
phase_centers = load_phase_centers(phase_center_file)  # Load phase centers from the file
process_all_ms_files(base_path, phase_centers)  # Process MS files with their phase centers

