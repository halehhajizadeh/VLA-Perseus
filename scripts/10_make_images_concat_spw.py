import sys
sys.path.append('.')
import time
import os
import numpy as np

path = '../data'
thresh = '1e-4'
pblim = '0.06'
nit = 5000
spw = [ 2, 3 , 4, 5, 6, 8, 15, 16, 17]

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


# pointings_folders = find_ms_folder(path + '/', "03")


pointings_folders =['../data/03:32:04.530001_+31.05.04.00000', '../data/03:25:30.000000_+29.29.59.99999']

pointings_folders_list= []
for i in pointings_folders:
    pointings_folders_list.append(i+'/data')

print(pointings_folders_list)
print('================================================================')
#----------------------------------------------------------------

ms_file_list = []
for j in np.array(pointings_folders_list):
    ms_file = find_ms_folder(j + '/', "19B-053")
    print ("MS File: ", ms_file)
    for k in ms_file:
        ms_file_list.append(j + '/' + k + '/products/targets.ms')

print('================================================================')
print(ms_file_list)

#----------------------------------------------------------------


for s in spw:
    tic = time.time()
    print(f"Stokes: I, s: {s} is started ...")

    img_filename = path + "/concat/total/Images/img" + str(nit) + "/tclean/" +  "spw" + str(s) + '-' + "-2.5arcsec-nit" + str(nit) + "-" + str(thresh) 

    tclean( vis=ms_file_list,
            field="PER_FIELD_*",
            spw=str(s),
            timerange="",
            uvrange="",
            antenna="",
            observation="",
            intent="",
            datacolumn="corrected",
            imagename=img_filename,
            imsize=[8000],
            cell=2.5,
            # phasecenter=phase_center,
            stokes='I',
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
    print(f"stokesI, s: {s} is finished!")
    print(f"Finshed the process in {round((toc-tic)/60)} minutes")
