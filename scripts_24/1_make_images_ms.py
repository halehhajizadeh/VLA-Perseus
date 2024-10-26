import os
from glob import glob
import shutil

# Define your base path
base_path = "/data/new/data/"

# Define the common parameters for tclean
def run_tclean(ms_file, img_filename, mosaic_name, phase_center):
    thresh = '2e-4'
    pblim = -0.001
    nit = 5000

    tclean(
        vis=ms_file,
        field="PER_FIELD_*",
        timerange="",
        uvrange="",
        antenna="",
        observation="",
        intent="",
        datacolumn="corrected",
        imagename=img_filename,
        imsize=[4096],
        cell="2.5arcsec",
        phasecenter=phase_center,
        stokes='I',
        specmode="mfs",
        gridder="awproject",
        mosweight=True,
        cfcache=f'/dev/shm/{mosaic_name}.cf',
        pblimit=pblim,
        deconvolver="mtmfs",
        pbcor=True,
        weighting="briggs",
        robust=0.5,
        niter=nit,
        gain=0.1,
        threshold=thresh,
        # cycleniter=200,
        cyclefactor=1,
        parallel=True,
        # psterm=True,
        nterms=2,
        rotatepastep=5.0,
        interactive=False
    )

# Function to find all directories and process the .ms files
def process_all_ms_files(base_path):
    # Find all subdirectories inside base_path
    dirs = glob(os.path.join(base_path, "*/"))
    
    for directory in dirs:
        # Find the .ms file ending with '_calibrated.ms' in each directory
        ms_files = glob(os.path.join(directory, "*_calibrated.ms"))
        
        if ms_files:
            ms_file = ms_files[0]  # Assuming only one .ms file in each directory
            img_filename = os.path.join(directory, "clean_image")  # Define a unique image name
            mosaic_name = os.path.basename(directory).split('.')[0]  # Generate mosaic name from directory name
            
            # Set a dummy phase_center; replace this with actual phase_center if known
            phase_center = "J2000 00:00:00.000 +00.00.00.000"
            
            # Run tclean
            print(f"Running tclean on {ms_file}")
            run_tclean(ms_file, img_filename, mosaic_name, phase_center)

# Execute the function
process_all_ms_files(base_path)
