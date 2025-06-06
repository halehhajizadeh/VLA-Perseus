import sys
import time
import os

sys.path.append('.')

thresh = '2e-4'
pblim = 0.06
nit = 5000
spw = [
       2,
       3 , 
       4, 
       5, 
       6, 
       8, 
       15,
       16, 
       17
       ]

# phase_center = 'J2000 03:32:04.530001 +31.05.04.00000'
# phase_center = 'J2000 03:36:00.000000 +30.30.00.00001'
# phase_center = 'J2000 03:25:30.000000 +29.29.59.99999'
phase_center = 'J2000 03:23:30.000001 +31.30.00.00000'

# specific_dirs = '03:32:04.530001_+31.05.04.00000/data/'
# specific_dirs =  '03:36:00.000000_+30.30.00.00001/data/' 
# specific_dirs =  '03:25:30.000000_+29.29.59.99999/data/'
specific_dirs =  '03:23:30.000001_+31.30.00.00000/data/'

def find_calibrated_files(base_directory, specific_dirs):
    calibrated_files = []
    full_path = os.path.join(base_directory, specific_dirs)
    if os.path.exists(full_path) and os.path.isdir(full_path):
        for root, dirs, files in os.walk(full_path):
            products_path = os.path.join(root, 'products')
            if os.path.exists(products_path) and os.path.isdir(products_path):
                for file in os.listdir(products_path):
                    if file.startswith('19B-053') and file.endswith('_calibrated.ms'):
                        calibrated_files.append(os.path.join(products_path, file))
    return calibrated_files

base_directory = '../data/'

ms_file_list = find_calibrated_files(base_directory, specific_dirs)

print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
for file in ms_file_list:
    print(file)
print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')

stokes1 = [
        # 'I',
        # 'Q',
        'U'
          ]

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

# Ensure ms_file_list is not empty before proceeding
if not ms_file_list:
    raise ValueError("No calibrated .ms files found! Please check the directory path.")

for stok in stokes1:
    for s in spw:
        for channel in channels:
            tic = time.time()
            print(f"stokes: {stok}, s: {s}, channel: {channel} is started ...")

            img_filename = os.path.join("../data/concat/", "03:23:30.000001_+31.30.00.00000/", "Images/img" + str(nit) + "/tclean/", "spw" + str(s) + '-' + str(channel) + "-2.5arcsec-nit" + str(nit) + "-" + str(thresh) + "-" + str(stok))

            spw_param = str(s) + ':' + channel  # Construct SPW parameter

            try:
                tclean(vis=ms_file_list,
                       field="PER_FIELD_*",
                       spw=spw_param,
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
                    #    nterms=2,
                    #    rotatepastep=5.0,
                       interactive=False,
                    #    restart=True,
                    #    calcres=True,
                    #    calcpsf=True,
                       )
            except Exception as e:
                print(f"Error processing SPW {spw_param}: {e}")
                raise

            toc = time.time()
            print(f"stokes: {stok}, s: {s}, channel: {channel} is finished!")
            print(f"Finished the process in {round((toc-tic)/60)} minutes")
