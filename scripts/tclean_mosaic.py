import sys
sys.path.append('.')
from configs import path, phase_center, nit, thresh, threedigits
import shutil
import os
from glob import glob

filename = path+'/targets.ms'

imagename= threedigits + '-mosaic-fieldAll-2.5arc-'+str(int)+'-spw1pb0.2'

if os.path.exists(path+"/Images_new/"+imagename+".image.fits"):
    os.remove(path+"/Images_new/"+imagename+".image.fits")

flist = glob(path+'/Images_new/'+imagename)
for images in flist:
    shutil.rmtree(images)


tclean(vis=filename,
       field="",
       spw="16:5~55",
       timerange="",
       uvrange="",
       antenna="",
       observation="",
       intent="",
       datacolumn="corrected",
       imagename=path+"/Images_new/"+imagename,
       imsize=[4096],
       cell="2.5arcsec",
       phasecenter=phase_center,
       stokes="I",
       projection="SIN",
       specmode="mfs",
       gridder="awproject",
       mosweight=True,
       cfcache="",
       pblimit=0.06,
       normtype="flatnoise",
       deconvolver="hogbom",
       restoration=True,
       restoringbeam=[],
       pbcor=True,
       outlierfile="",
       weighting="briggs",
       robust=0.5,
       npixels=2,
       uvtaper=[],
       niter=nit,
       gain=0.1,
       threshold=thresh,
       nsigma=0.0,
       cycleniter=-1,
       cyclefactor=1.0,
       restart=True,
       calcres=True,
       calcpsf=True,
       parallel=True,
       interactive=False)



exportfits(path+"/Images_new/"+imagename+".image", path+"/Images_new/"+imagename+".image.fits")