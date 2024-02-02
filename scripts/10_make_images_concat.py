import sys
sys.path.append('.')
import time
import os
import path, phasecenter, threedigits, thresh, pblim, nit

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


folders_list = find_ms_folder(path, "19B-053")

ms_list = []
for i in folders_list:
    ms_list.append(i+'/products/targets.ms')

print(ms_list)


spw = [ 2, 3 , 4, 5, 6, 8, 15, 16, 17]

stokes1 = [
        'I',
        'Q',
        'U'
          ]

channels = ['00~07', '08~15', '16~23', '24~31', '32~39', '40~47', '48~55', '56~63']

for stok in stokes1:
    for s in spw:
        for channel in channels:
            tic = time.time()
            print(f"stokes: {stok}, s: {s}, channel: {channel} is started ...")

            img_filename = path + "/concat/"+str(threedigits)+"/Images/img" + str(nit) + "/tclean/" + str(threedigits) + "-spw" + str(s) + '-' + str(channel) + "-2.5arcsec-nit" + str(nit) + "-" + str(thresh) + "-" + str(stok)

            tclean( vis=ms_list,
                    field="PER_FIELD_*",
                    spw=str(s) + ':' + channel,
                    timerange="",
                    uvrange="",
                    antenna="",
                    observation="",
                    intent="",
                    datacolumn="corrected",
                    imagename=img_filename,
                    imsize=[4320],
                    cell=2.5,
                    phasecenter=phase_center,
                    stokes=stok,
                    projection="SIN",
                    specmode="mfs",
                    gridder="mosaic",
                    mosweight=True,
                    cfcache="",
                    pblimit=pblim,
                    normtype="flatnoise",
                    deconvolver="hogbom",
                    restoration=True,
                    restoringbeam=[],
                    pbcor=True,
                    outlierfile="",
                    weighting="briggs",
                    robust=0.5,
                    npixels=0,
                    niter=nit,
                    gain=0.1,
                    threshold=thresh,
                    nsigma=0,
                    cycleniter=500,
                    cyclefactor=1,
                    parallel=False)
        
            toc = time.time()
            print(f"stokes: {stok}, s: {s}, channel: {channel} is finished!")
            print(f"Finshed the process in {round((toc-tic)/60)} minutes")
