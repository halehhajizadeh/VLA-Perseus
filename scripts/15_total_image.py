import sys
sys.path.append('.')
import shutil
import os
from glob import glob
from configs import path, phase_center, nit, thresh, threedigits, pblim

filename = path+'/targets.ms'

Stoke = 'I'

imagename= threedigits + '-mosaic-fieldALL-Stokes'+str(Stoke)+'-2.5arc-'+str(nit)+'-'+str(thresh)+'-spwALL-pb'+str(pblim)+'-cyclenit500'

if os.path.exists(path+"/Images/"+imagename+".image.fits"):
    os.remove(path+"/Images/"+imagename+".image.fits")

flist = glob(path+'/Images/'+imagename)
for images in flist:
    shutil.rmtree(images)


tclean(vis=filename,
       field="",
       spw="",
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