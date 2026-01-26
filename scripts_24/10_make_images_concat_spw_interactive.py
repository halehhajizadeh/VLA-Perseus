import os
import time
import sys
import shutil
import glob
sys.path.append('.')

# === Parameters ===
thresh = '1e-5'
pblim = -0.001
nit = 15000

base_path = '/lustre/aoc/observers/nm-12934/VLA-Perseus/data/new/data/'

# ============================================================================
# USER SELECTIONS - Comment out what you DON'T want to process
# ============================================================================

# === Select ONE mosaic (comment out the others) ===
# selected_mosaic = '03:26:24.057_+30.35.58.881'
# selected_mosaic = '03:29:12.973_+31.48.05.579'
# selected_mosaic = '03:31:12.055_+29.47.58.916'
# selected_mosaic = '03:39:12.060_+31.23.58.844'
# selected_mosaic = '03:40:00.063_+32.23.58.799'
# selected_mosaic = '03:42:00.057_+30.29.58.885'
selected_mosaic = '03:45:12.060_+31.41.58.831'
# selected_mosaic = '03:45:36.064_+32.47.58.780'

# === Select MS directories (comment out the ones you DON'T want) ===

# For mosaic: 03:26:24.057_+30.35.58.881
# selected_ms_dirs = [
#     '24A-376.sb45387559.eb45519359.60419.617289120375',
#     '24A-376.sb45326471.eb45364730.60407.79050123843',
#     '24A-376.sb45274301.eb45298942.60377.89050475694',
    # '24A-376.sb45274301.eb45320543.60392.77890695602'
# ]

# For mosaic: 03:29:12.973_+31.48.05.579
# selected_ms_dirs = [
    # '24A-376.sb45326158.eb45364719.60407.70739606481',
    # '24A-376.sb45258229.eb45320541.60392.6957443287',
    # '24A-376.sb45258229.eb45299201.60381.83744690972'
    # 
    
    # ]

# For mosaic: 03:31:12.055_+29.47.58.916
# selected_ms_dirs = [
#     '24A-376.sb45274699.eb45355183.60406.65306927083',
#     '24A-376.sb45326823.eb45330487.60398.69350814815',
#     '24A-376.sb45274699.eb45316354.60388.70691569445',
#     '24A-376.sb45274699.eb45340091.60402.74949883102'
# ]

# For mosaic: 03:39:12.060_+31.23.58.844
# selected_ms_dirs = [
#     '24A-376.sb45275457.eb45297613.60377.807340659725',
#     '24A-376.sb45387872.eb45480125.60416.76979049768',
#     '24A-376.sb45275457.eb45298960.60378.880123090275',
#     '24A-376.sb45327136.eb45355185.60406.738546782406'
# ]

# For mosaic: 03:40:00.063_+32.23.58.799
# selected_ms_dirs = [
#     '24A-376.sb45388185.eb45417364.60412.697942569444',
#     '24A-376.sb45275770.eb45320378.60391.775079722225',
#     '24A-376.sb45327449.eb45331461.60399.67654158565',
#     '24A-376.sb45275770.eb45308786.60386.74124510417'
# ]

# For mosaic: 03:42:00.057_+30.29.58.885
# selected_ms_dirs = [
#     '24A-376.sb45328466.eb45330489.60398.77661226851',
#     '24A-376.sb45276709.eb45316801.60388.83163046296',
#     '24A-376.sb45276709.eb45306373.60384.798636736115'
# ]

# For mosaic: 03:45:12.060_+31.41.58.831
selected_ms_dirs = [
#     '24A-376.sb45388498.eb45455607.60414.75498211806',
    '24A-376.sb45276396.eb45299199.60381.75428434028',
#     '24A-376.sb45276396.eb45305980.60384.715532013885',
#     '24A-376.sb45328153.eb45331463.60399.75970537037'
]

# For mosaic: 03:45:36.064_+32.47.58.780
# selected_ms_dirs = [
#     '24A-376.sb45276083.eb45308767.60385.71070592593',
#     '24A-376.sb45327762.eb45339078.60402.66413293981',
#     '24A-376.sb45276083.eb45308771.60385.85637064815'
# ]

# === Select SPWs (comment out the ones you DON'T want) ===
selected_spw = [
    # 2,
    # 3,
    # 4,
    # 5,
    # 6,
    8,
    # 15,
    # 16,
    # 17
]

# === Choose ONE mask to activate (optional) ===
# mask_name = base_path + '03:26:24.057_+30.35.58.881' + '/24A-376.sb45274301.eb45298942.60377.89050475694/5694_mask_final.image' #26
# mask_name = base_path + '03:29:12.973_+31.48.05.579' + '/24A-376.sb45258229.eb45320541.60392.6957443287/3287_mask_final.image' #29
# mask_name = base_path + '03:31:12.055_+29.47.58.916' + '/24A-376.sb45326823.eb45330487.60398.69350814815/4815_mask_final.image' #31
# mask_name = base_path + '03:39:12.060_+31.23.58.844' + '/24A-376.sb45387872.eb45480125.60416.76979049768/9768_mask_final.image' #39
# mask_name = base_path + '03:40:00.063_+32.23.58.799' + '/24A-376.sb45388185.eb45417364.60412.697942569444/???_mask_final.image' #40
# mask_name = base_path + '03:42:00.057_+30.29.58.885' + '/24A-376.sb45328466.eb45330489.60398.77661226851/6851_mask_final.image' #42
mask_name = base_path + '03:45:12.060_+31.41.58.831' + '/24A-376.sb45388498.eb45455607.60414.75498211806/1806_mask_final.image' #45:12
# mask_name = base_path + '03:45:36.064_+32.47.58.780' + '/24A-376.sb45327762.eb45339078.60402.66413293981/3981_mask_final.image' #45:36

# ============================================================================
# AUTO-SETUP - No need to modify below
# ============================================================================

# Phase centers for each mosaic
phase_centers = {
    # '03:26:24.057_+30.35.58.881': 'J2000 03:26:24.057 +30.35.58.881',
    # '03:29:12.973_+31.48.05.579': 'J2000 03:29:12.973 +31.48.05.579',
    # '03:31:12.055_+29.47.58.916': 'J2000 03:31:12.055 +29.47.58.916',
    # '03:39:12.060_+31.23.58.844': 'J2000 03:39:12.060 +31.23.58.844',
    # '03:40:00.063_+32.23.58.799': 'J2000 03:40:00.063 +32.23.58.799',
    # '03:42:00.057_+30.29.58.885': 'J2000 03:42:00.057 +30.29.58.885',
    '03:45:12.060_+31.41.58.831': 'J2000 03:45:12.060 +31.41.58.831',
    # '03:45:36.064_+32.47.58.780': 'J2000 03:45:36.064 +32.47.58.780'
}

phase_center = phase_centers[selected_mosaic]
base_directory = base_path + selected_mosaic

# === Print configuration ===
print('='*80)
print('CONFIGURATION:')
print('='*80)
print(f"Mosaic: {selected_mosaic}")
print(f"Phase center: {phase_center}")
print(f"\nMS directories ({len(selected_ms_dirs)}):")
for ms_dir in selected_ms_dirs:
    print(f"  - {ms_dir}")
print(f"\nSPWs ({len(selected_spw)}): {selected_spw}")
print(f"\nTotal jobs: {len(selected_ms_dirs) * len(selected_spw)}")
print('='*80)


# === Run tclean ===
print('\n' + '='*80)
print('STARTING IMAGING')
print('='*80)

for ms_dir in selected_ms_dirs:
    ms_dir_path = os.path.join(base_directory, ms_dir)

    # Look for _calibrated.ms file
    ms_path = None
    for item in os.listdir(ms_dir_path):
        if item.endswith('_calibrated.ms'):
            ms_path = os.path.join(ms_dir_path, item)
            break

    if not ms_path:
        print(f"\nWarning: No _calibrated.ms found in {ms_dir}, skipping...")
        continue

    ms_name = os.path.basename(ms_path).replace('_calibrated.ms', '')

    for s in selected_spw:
        tic = time.time()
        print(f"\nStokes: I, {ms_name}, spw: {s} is started ...")

        output_dir = f"/lustre/aoc/observers/nm-12934/VLA-Perseus/data/new/data/concat/{selected_mosaic}/Images/spw/{ms_name}/tclean/spw{s}"
        os.makedirs(output_dir, exist_ok=True)

        img_filename = output_dir + '/' + f"{ms_name}_StokesI_spw{s}-2.5arcsec-nit{nit}-awproject"

        # Delete existing output files if they exist
        for old_file in glob.glob(img_filename + '*'):
            if os.path.isdir(old_file):
                shutil.rmtree(old_file)
                print(f"Deleted existing directory: {old_file}")
            elif os.path.isfile(old_file):
                os.remove(old_file)
                print(f"Deleted existing file: {old_file}")

        tclean(vis=ms_path,
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
               cfcache=f"/dev/shm/{ms_name}_spw{s}.cf",
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
               nsigma=3,
               rotatepastep=5.0,
               interactive=False,
               psfcutoff=0.5,
               mask=mask_name
              )

        toc = time.time()
        print(f"Stokes: I, {ms_name}, spw: {s} is finished in {round((toc - tic)/60, 2)} minutes")

print('\n' + '='*80)
print('ALL IMAGING JOBS COMPLETED!')
print('='*80)
