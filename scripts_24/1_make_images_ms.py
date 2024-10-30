import os
from glob import glob
import shutil

# Define your base path
base_path = "../data/new/data/"

# Define the common parameters for tclean
def run_tclean(ms_file, img_filename, mosaic_name):
    thresh = '2e-4'
    pblim = -0.001
    nit = 5000

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
        phasecenter="",
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
        nsigma=3,
        threshold=thresh,
        # cycleniter=200,
        psfcutoff=0.5,
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
            
            # Run tclean
            print(f"Running tclean on {ms_file}")
            run_tclean(ms_file, img_filename, mosaic_name)

# Execute the function
process_all_ms_files(base_path)
