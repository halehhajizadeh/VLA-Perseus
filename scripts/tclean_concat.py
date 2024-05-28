import sys
sys.path.append('.')
import shutil
import os
from glob import glob

path='../data/03:34:30.000000_+31.59.59.99999/data/'

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
for folder in folders_list:
    products_path = os.path.join(folder, 'products')
    for file_name in os.listdir(products_path):
        if file_name.endswith('_calibrated.ms'):
            ms_list.append(os.path.join(products_path, file_name))

print(ms_list)


pblim = 0.001
nit = 5000
Stoke = 'I'
thresh='1e-4'
phase_center='J2000 03:36:30.200000 +32.18.28.00000'
imagename = 'mosaic3'


tclean(vis=ms_list,
       field="PER_FIELD_*, J0336+3218",
       spw="",
       timerange="",
       antenna="",
       observation="",
       intent="",
       datacolumn="corrected",
       imagename=path+imagename,
       imsize=[5000],
       cell="2.5arcsec",
       phasecenter=phase_center,
       stokes=Stoke,
       projection="SIN",
       specmode="mfs",
       gridder="awproject",
       mosweight=True,
       cfcache="",
       pblimit=pblim,
       normtype="flatnoise",
       deconvolver="mtmfs",
       restoration=True,
       restoringbeam=[],
       pbcor=True,
       outlierfile="",
       weighting="briggs",
       robust=0.5,
       npixels=0,
       uvtaper=[],
       niter=nit,
       gain=0.1,
       threshold=thresh,
       nsigma=0,
       nterms=2,
       rotatepastep=5.0,
       cycleniter=200,
       cyclefactor=1,
       restart=True,
       calcres=True,
       calcpsf=True,
       parallel=True,
       interactive=True)


