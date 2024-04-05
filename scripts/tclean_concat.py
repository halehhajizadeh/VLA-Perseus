import sys
sys.path.append('.')
import shutil
import os
from glob import glob

path='../data/03:32:04.530001_+31.05.04.00000/data/'

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


pblim = 0.06
nit = 5000
Stoke = 'Q'
thresh='1e-4'
phase_center='J2000 03:32:04.530001 +31.05.04.00000'

imagename = '1original-'+'mosaic-fieldAll-Stokes'+str(Stoke)+'-2.5arc-'+str(nit)+'-'+str(thresh)+'-spw16-pb'+str(pblim)+'-cyclenit500'


tclean(vis=ms_list,
       field="PER_FIELD_*",
       spw="16:5~60",
       timerange="",
       uvrange=">75m",
       antenna="",
       observation="",
       intent="",
       datacolumn="corrected",
       imagename=path+'concat/03:32:04.530001_+31.05.04.00000/'+imagename,
       imsize=[4320],
       cell="2.5arcsec",
       phasecenter=phase_center,
       stokes=Stoke,
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
       uvtaper=[],
       niter=nit,
       gain=0.1,
       threshold=thresh,
       nsigma=0,
       cycleniter=500,
       cyclefactor=1,
       restart=True,
       calcres=True,
       calcpsf=True,
       parallel=False,
       interactive=False)

exportfits(path+'concat/03:32:04.530001_+31.05.04.00000/'+imagename+".image", path+'concat/03:32:04.530001_+31.05.04.00000/'+imagename+".image.fits")

