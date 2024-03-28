import sys
sys.path.append('.')
import shutil
import os
from glob import glob
from configs import path, phase_center, nit, thresh, threedigits


msfilename= path + '/targets.ms'
pblim = 0.06
Stoke = 'Q'

image_name= '/test1'



tclean(vis=msfilename,
       field="PER_FIELD_*",
       spw="15:0~7",
       timerange="",
       uvrange="",
       antenna="",
       observation="",
       intent="",
       datacolumn="corrected",
       imagename=path+image_name,
       imsize=[4320],
       cell=2.5,
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

exportfits(path+"/Images/"+image_name+".image", path+"/Images/"+image_name+".image.fits")

