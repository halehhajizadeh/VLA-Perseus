import sys
sys.path.append('.')
import shutil
import os
from glob import glob
# from configs import path, phase_center, nit, thresh, threedigits

path = '../data'
phase_center = 'J2000 03:32:04.530001 +31.05.04.00000'
thresh = '1e-4'
nit = 5000
threedigits = '03:32:04.530001_+31.05.04.00000'
pblim = 0.06

path = '../data/03:32:04.530001_+31.05.04.00000/19B-053_2019_12_15_T07_36_56.546/products'
filename = path + '/19B-053.sb37264871.eb37595549.58832.22860825231_calibrated.ms/'


Stoke = 'I'

imagename= threedigits + '-mosaic-fieldAll-Stokes'+str(Stoke)+'-2.5arc-'+str(nit)+'-'+str(thresh)+'-spw16-pb'+str(pblim)+'-cyclenit500'

# if os.path.exists(path+"/Images/"+imagename+".image.fits"):
#     os.remove(path+"/Images/"+imagename+".image.fits")

# flist = glob(path+'/Images/'+imagename)
# for images in flist:
#     shutil.rmtree(images)


tclean(vis=filename,
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
       nsigma=0,
       cycleniter=500,
       cyclefactor=1,
       restart=True,
       calcres=True,
       calcpsf=True,
       parallel=False,
       interactive=False)

exportfits(path+"/Images/"+imagename+".image", path+"/Images/"+imagename+".image.fits")

