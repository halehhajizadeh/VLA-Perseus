import sys
sys.path.append('.')
from configs import path, phase_center, nit, thresh, threedigits
import shutil
import os
from glob import glob

nit=100
filename = path+'/targets.ms'

imagename= threedigits + '-awproject-5000-fieldAll-2.5arc-'+str(nit)+'-spw16-pb-0.01-false'

if os.path.exists(path+"/Images_new/"+imagename+".image.fits"):
    os.remove(path+"/Images_new/"+imagename+".image.fits")

flist = glob(path+'/Images_new/'+imagename)
for images in flist:
    shutil.rmtree(images)

print('nint is ' + str(nit))

tclean(vis=filename,
       field="PER_FIELD_*",
       spw="16:5~60",
       timerange="",
       uvrange="",
       antenna="",
       observation="",
       intent="",
       datacolumn="corrected",
       imagename=path+"/Images_new/"+imagename,
       imsize=[5000],
       cell="2.5arcsec",
       phasecenter=phase_center,
       stokes="I",
       projection="SIN",
       specmode="mfs",
       gridder="awproject",
       mosweight=True,
       cfcache="",
       pblimit=0.009,
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
       nsigma=0.0,
       cycleniter=-1,
       cyclefactor=1.0,
       restart=True,
       calcres=False,
       calcpsf=True,
    #    parallel=True,
       interactive=False,
       wbawp=False,
       rotatepastep=5.0,
       conjbeams=False)



exportfits(path+"/Images_new/"+imagename+".image", path+"/Images_new/"+imagename+".image.fits")
