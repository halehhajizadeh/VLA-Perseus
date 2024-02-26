import sys
sys.path.append('.')
import time
import os

path = '../data'
thresh = '1e-4'
pblim = '0.06'
nit = 5000
spw = [ 2, 3 , 4, 5, 6, 8, 15, 16, 17]
stokes1 = [
        'I',
        # 'Q',
        # 'U'
          ]


def find_ms_folder(directory, startswith='19B-053', endswith=''):
    """
    Finds names of ms files in a directroy.

    directory (str): The directory to search
    startswith (str): The beginning of the file to search
    endswith (str): The end of the file to search

    Returns:
    str : An array including the name of the ms files found.
    """
    folders_list = []
    for file in os.listdir(directory):
        if file.startswith(startswith):
            if file.endswith(endswith):
                folders_list.append(os.path.join(directory, file))                
    return(folders_list)


pointings_folders = find_ms_folder(path + '/', "03")

pointings_folders_list= []
for i in pointings_folders:
    pointings_folders_list.append(i+'/data')

print(pointings_folders_list)

#----------------------------------------------------------------

ms_file_list = []
for j in pointings_folders_list:
    ms_file = find_ms_folder(j + '/', "19B-053", ".ms")
    ms_file_list.append(j + '/' + ms_file)

print(ms_file_list)

#----------------------------------------------------------------

# for stok in stokes1:
#     for s in spw:
#         tic = time.time()
#         print(f"stokes: {stok}, s: {s}, channel: {channel} is started ...")

#         img_filename = path + "/concat/"+str(threedigits)+"/Images/img" + str(nit) + "/tclean/" + str(threedigits) + "-spw" + str(s) + '-' + str(channel) + "-2.5arcsec-nit" + str(nit) + "-" + str(thresh) + "-" + str(stok)

#         tclean( vis=ms_file_list,
#                 field="PER_FIELD_*",
#                 spw=str(s) + ':' + '0~62',
#                 timerange="",
#                 uvrange="",
#                 antenna="",
#                 observation="",
#                 intent="",
#                 datacolumn="corrected",
#                 imagename=img_filename,
#                 imsize=[4320],
#                 cell=2.5,
#                 # phasecenter=phase_center,
#                 stokes=stok,
#                 projection="SIN",
#                 specmode="mfs",
#                 gridder="mosaic",
#                 mosweight=True,
#                 cfcache="",
#                 pblimit=pblim,
#                 normtype="flatnoise",
#                 deconvolver="hogbom",
#                 restoration=True,
#                 restoringbeam=[],
#                 pbcor=True,
#                 outlierfile="",
#                 weighting="briggs",
#                 robust=0.5,
#                 npixels=0,
#                 niter=nit,
#                 gain=0.1,
#                 threshold=thresh,
#                 nsigma=0,
#                 cycleniter=500,
#                 cyclefactor=1,
#                 parallel=False)
    
#         toc = time.time()
#         print(f"stokes: {stok}, s: {s}, channel: {'0~62'} is finished!")
#         print(f"Finshed the process in {round((toc-tic)/60)} minutes")
