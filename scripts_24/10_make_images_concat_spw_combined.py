import os
import time
import sys
import shutil
import glob
sys.path.append('.')

# === Parameters ===
thresh = '1e-5'
pblim = -0.001
nit = 20000
spw = [
    2,
    3,
    4,
    5,
    6,
    8,
    15,
    16,
    17
]

# === Choose ONE phase center to activate ===
phase_center = 'J2000 03:26:24.057 +30.35.58.881'
# phase_center = 'J2000 03:29:12.973 +31.48.05.579'
# phase_center = 'J2000 03:31:12.055 +29.47.58.916'
# phase_center = 'J2000 03:39:12.060 +31.23.58.844'
# phase_center = 'J2000 03:40:00.063 +32.23.58.799'
# phase_center = 'J2000 03:42:00.057 +30.29.58.885'
# phase_center = 'J2000 03:45:12.060 +31.41.58.831'
# phase_center = 'J2000 03:45:36.064 +32.47.58.780'

mosaic_name = '03:26:24.057_+30.35.58.881'
# mosaic_name = '03:29:12.973_+31.48.05.579'
# mosaic_name = '03:31:12.055_+29.47.58.916'
# mosaic_name = '03:39:12.060_+31.23.58.844'
# mosaic_name = '03:40:00.063_+32.23.58.799'
# mosaic_name = '03:42:00.057_+30.29.58.885'
# mosaic_name = '03:45:12.060_+31.41.58.831'
# mosaic_name = '03:45:36.064_+32.47.58.780'

base_directory = '/lustre/aoc/observers/nm-12934/VLA-Perseus/data/new/data/' + mosaic_name

# === Choose ONE mask to activate ===
mask_name = base_directory + '/24A-376.sb45274301.eb45298942.60377.89050475694/5694_mask_final.image' #26
# mask_name = base_directory + '/24A-376.sb45258229.eb45320541.60392.6957443287/3287_mask_final.image' #29
# mask_name = base_directory + '/24A-376.sb45326823.eb45330487.60398.69350814815/4815_mask_final.image' #31
# mask_name = base_directory + '/24A-376.sb45387872.eb45480125.60416.76979049768/9768_mask_final.image' #39
# mask_name = base_directory + '/24A-376.sb45328466.eb45330489.60398.77661226851/6851_mask_final.image' #42
# mask_name = base_directory + '/24A-376.sb45388498.eb45455607.60414.75498211806/1806_mask_final.image' #45:12
# mask_name = base_directory + '/24A-376.sb45327762.eb45339078.60402.66413293981/3981_mask_final.image' #45:36

# === Find calibrated MS files (skips 'ignore' directory) ===
def find_calibrated_files(base_directory):
    calibrated_files = []
    for subfolder in os.listdir(base_directory):
        # Skip the 'ignore' directory
        if subfolder.lower() == 'ignore':
            continue
        sub_path = os.path.join(base_directory, subfolder)
        if os.path.isdir(sub_path) and subfolder.startswith('24A'):
            for file in os.listdir(sub_path):
                if file.endswith('_calibrated.ms'):
                    calibrated_files.append(os.path.join(sub_path, file))
    return calibrated_files

ms_file_list = find_calibrated_files(base_directory)

# === Print configuration ===
print('='*80)
print('JOINT IMAGING - Combining all measurement sets')
print('='*80)
print(f"Mosaic: {mosaic_name}")
print(f"Phase center: {phase_center}")
print(f"\nMS files to combine ({len(ms_file_list)}):")
for ms_file in ms_file_list:
    print(f"  - {os.path.basename(ms_file)}")
print(f"\nSPWs ({len(spw)}): {spw}")
print(f"\nTotal imaging jobs: {len(spw)} (one per SPW)")
print('='*80)

if len(ms_file_list) == 0:
    print("ERROR: No calibrated MS files found!")
    sys.exit(1)

# === Run tclean combining ALL MS files ===
for s in spw:
    tic = time.time()
    print(f"\nStokes: I, COMBINED, spw: {s} is started ...")
    print(f"Combining {len(ms_file_list)} measurement sets")

    output_dir = f"/lustre/aoc/observers/nm-12934/VLA-Perseus/data/new/data/concat/{mosaic_name}/Images/spw/combined/tclean/spw{s}"
    os.makedirs(output_dir, exist_ok=True)

    img_filename = output_dir + '/' + f"{mosaic_name}_StokesI_spw{s}-2.5arcsec-nit{nit}-awproject-combined"

    # Delete existing output files if they exist
    for old_file in glob.glob(img_filename + '*'):
        if os.path.isdir(old_file):
            shutil.rmtree(old_file)
            print(f"Deleted existing directory: {old_file}")
        elif os.path.isfile(old_file):
            os.remove(old_file)
            print(f"Deleted existing file: {old_file}")

    tclean(vis=ms_file_list,  # Pass list of ALL MS files for joint imaging
           field="PER_FIELD_*",
           spw=str(s),
           datacolumn="corrected",
           imagename=img_filename,
           imsize=[4096],
           cell="2.5arcsec",
           phasecenter=phase_center,
           stokes='I',
           specmode="mfs",
           gridder="awproject",
           mosweight=True,
           cfcache=f"/dev/shm/combined_spw{s}.cf",
           pblimit=pblim,
           deconvolver="mtmfs",
           pbcor=True,
           weighting="briggs",
           robust=0.5,
           wbawp=True,
           conjbeams=True,
           niter=nit,
           gain=0.1,
           threshold=thresh,
           cyclefactor=1,
           parallel=True,
           nterms=2,
        #    nsigma=3,
           rotatepastep=5.0,
           interactive=False,
           psfcutoff=0.5,
           mask=mask_name
          )

    toc = time.time()
    print(f"Stokes: I, COMBINED, spw: {s} is finished in {round((toc - tic)/60, 2)} minutes")

print('\n' + '='*80)
print('ALL JOINT IMAGING JOBS COMPLETED!')
print('='*80)
