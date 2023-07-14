import sys
sys.path.append('.')
from configs import path
import shutil
import os
from glob import glob

filename = path+'/targets.ms'

imagename= '546-awproject-fieldAll-5arc-10000-spw1pb0.2'

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
       cell="5arcsec",
       phasecenter="J2000 03:32:54.609000 +31.11.15.01999",
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
       niter=10000,
       gain=0.1,
       threshold=1e-4,
       nsigma=0.0,
       cycleniter=-1,
       cyclefactor=1.0,
       restart=True,
       calcres=True,
       calcpsf=True,
       parallel=False,
       interactive=False)



exportfits(path+"/Images_new/"+imagename+".image", path+"/Images_new/"+imagename+".image.fits")
