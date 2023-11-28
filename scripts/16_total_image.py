import sys
sys.path.append('.')
import shutil
import os
from glob import glob
# from configs import path, phase_center, nit, thresh, threedigits, pblim



path = '../data'
phase_center = 'J2000 03:34:30.000000 +31.59.59.99999'
thresh = '1e-4'
nit = 5000
threedigits = '03:34:30.000000_+31.59.59.99999'
pblim = 0.06




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
    # ms_list.append(i+'/products/targets.ms')
    ms_list.append(i+'/*.ms')

print(ms_list)



Stoke = 'I'

imagename= threedigits + '-mosaic-fieldALL-Stokes'+str(Stoke)+'-2.5arc-'+str(nit)+'-'+str(thresh)+'-spw16-pb'+str(pblim)+'-cyclenit500'

if os.path.exists(path+"/Images/"+imagename+".image.fits"):
    os.remove(path+"/Images/"+imagename+".image.fits")

flist = glob(path+'/Images/'+imagename)
for images in flist:
    shutil.rmtree(images)


tclean(vis=ms_list,
       field="PER_FIELD_*",
       spw="16",
       timerange="",
       uvrange="",
       antenna="",
       observation="",
       intent="",
       datacolumn="corrected",
       imagename=path+"/Images/"+imagename,
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
       nsigma=3,
       cycleniter=500,
       cyclefactor=1,
       restart=True,
       calcres=True,
       calcpsf=True,
       parallel=False,
       interactive=False)

exportfits(path+"/Images/"+imagename+".image", path+"/Images/"+imagename+".image.fits")