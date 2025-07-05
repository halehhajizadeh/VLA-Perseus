import sys
import time
import os

sys.path.append('.')

thresh = '6e-5'
pblim = 0.06
nit = 7000


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


stokes1 = [
    'I',
    'Q',
    'U'
    ]  # or add 'I', 'Q' as needed

channels = [
    '00~07',
    '08~15', 
    '16~23',
    '24~31', 
    '32~39', 
    '40~47', 
    '48~55', 
    '56~63'
]

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



# Base path
base_directory = '/lustre/aoc/observers/nm-12934/VLA-Perseus/data/new/data/' + mosaic_name



mask_name = base_directory + '/24A-376.sb45274301.eb45298942.60377.89050475694/5694_mask_final.image' #J2000 03:26:24.057 +30.35.58.881
# mask_name = base_directory + '/24A-376.sb45258229.eb45320541.60392.6957443287/3287_mask_final.image' #J2000 03:29:12.973 +31.48.05.579
# mask_name = base_directory + '/24A-376.sb45326823.eb45330487.60398.69350814815/4815_mask_final.image' #J2000 03:31:12.055 +29.47.58.916
# mask_name = base_directory + '/24A-376.sb45387872.eb45480125.60416.76979049768/9768_mask_final.image' #J2000 03:39:12.060 +31.23.58.844
# mask_name = base_directory + '/24A-376.sb45274301.eb45298942.60377.89050475694/5694_mask_final.image' #J2000 03:40:00.063 +32.23.58.799
# mask_name = base_directory + '/24A-376.sb45328466.eb45330489.60398.77661226851/6851_mask_final.image' #J2000 03:42:00.057 +30.29.58.885
# mask_name = base_directory + '/24A-376.sb45388498.eb45455607.60414.75498211806/1806_mask_final.image' #J2000 03:45:12.060 +31.41.58.831
# mask_name = base_directory + '/24A-376.sb45327762.eb45339078.60402.66413293981/9881_mask_final.image' #J2000 03:45:36.064 +32.47.58.780

# Find _calibrated.ms files inside 24A* subdirectories
def find_calibrated_files(base_directory):
    calibrated_files = []
    for subfolder in os.listdir(base_directory):
        sub_path = os.path.join(base_directory, subfolder)
        if os.path.isdir(sub_path) and subfolder.startswith('24A'):
            for file in os.listdir(sub_path):
                if file.endswith('_calibrated.ms'):
                    calibrated_files.append(os.path.join(sub_path, file))
    return calibrated_files

# Get MS file list
ms_file_list = find_calibrated_files(mosaic_name)

# Print MS file list
print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
for file in ms_file_list:
    print(file)
print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')

# Check before proceeding
if not ms_file_list:
    raise ValueError("No calibrated .ms files found! Please check the directory path.")

# Run tclean loops
for stok in stokes1:
    for s in spw:
        for channel in channels:
            tic = time.time()
            print(f"stokes: {stok}, s: {s}, channel: {channel} is started ...")

            img_filename = os.path.join(
                base_directory, 'concat/',
                mosaic_name,
                "Images/img/" ,
                "tclean",
                f"spw{s}-{channel}-2.5arcsec-nit{nit}-{thresh}-{stok}"
            )

            spw_param = f"{s}:{channel}"

            try:
                tclean(vis=ms_file_list,
                       field="PER_FIELD_*",
                       spw=spw_param,
                       datacolumn="corrected",
                       imagename=img_filename,
                       imsize=[4096],
                       cell="2.5arcsec",
                       phasecenter=phase_center,
                       stokes=stok,
                       specmode="mfs",
                       gridder="mosaic",
                       mosweight=True,
                       pblimit=pblim,
                       deconvolver="hogbom",
                       pbcor=True,
                       weighting="briggs",
                       robust=0.5,
                       niter=nit,
                       gain=0.1,
                       threshold=thresh,
                       cycleniter=500,
                       cyclefactor=1,
                       interactive=False,
                       mask = mask_name
                       )
            except Exception as e:
                print(f"Error processing SPW {spw_param}: {e}")
                raise

            toc = time.time()
            print(f"stokes: {stok}, s: {s}, channel: {channel} is finished!")
            print(f"Finished the process in {round((toc - tic) / 60)} minutes")
