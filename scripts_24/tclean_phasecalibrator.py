import os
import shutil
from glob import glob
from casatasks import tclean

def run_tclean(ms_list, img_filename, mosaic_name, phasecenter):
    thresh = '9e-5'
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

    tclean(
        vis=ms_list,
        field="PER_FIELD_*",
        timerange="",
        spw="",
        uvrange="",
        antenna="",
        observation="",
        intent="",
        datacolumn="corrected",
        imagename=img_filename,
        imsize=[8192],  # You can adjust this
        cell="2.5arcsec",
        phasecenter=phasecenter,
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
        parallel=True,
        nterms=2,
        rotatepastep=5.0,
        interactive=False
    )

# === Define base directories ===
dirs = [
    "/lustre/aoc/observers/nm-12934/VLA-Perseus/data/03:34:30.000000_+31.59.59.99999/data",
    "/lustre/aoc/observers/nm-12934/VLA-Perseus/data/new/data/03:40:00.063_+32.23.58.799"
]

# === Define phasecenter (from your screenshot) ===
phasecenter = "J2000 03:36:29.7 +32.18.26"

# === Collect all *_calibrated.ms files from subdirs ===
all_ms_files = []

for base_dir in dirs:
    for root, subdirs, _ in os.walk(base_dir):
        for sub in subdirs:
            if sub.startswith(("19B", "24A")):
                ms_path = os.path.join(root, sub)
                ms_files = glob(os.path.join(ms_path, "*_calibrated.ms"))
                all_ms_files.extend(ms_files)

# === Print and verify all files before running ===
print("Total Measurement Sets to include in mosaic:")
for ms in all_ms_files:
    print(ms)

# === Define output image path ===
image_dir = "/lustre/aoc/observers/nm-12934/VLA-Perseus/data/new/data/03:40:00.063_+32.23.58.799/Images"
os.makedirs(image_dir, exist_ok=True)
image_name = os.path.join(image_dir, "perseus_mosaic_image")

# === Run tclean on all MS files combined ===
run_tclean(all_ms_files, image_name, "perseus_mosaic", phasecenter)
