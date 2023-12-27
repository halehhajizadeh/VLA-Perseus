import sys
sys.path.append('.')
import shutil
import os
from glob import glob
from configs import path, phase_center, nit, thresh, threedigits, msfilename

# path = '../data'
# phase_center = 'J2000 03:25:30.000000 +29.29.59.99999'
# thresh = '1e-4'
# nit = 5000
# threedigits = '03:25:30.000000_+29.29.59.99999'
pblim = 0.06

# path = '../data/19B-053_2020_01_09_T02_00_58.482/products'
# filename = path + '/19B-053.sb37665557.eb37682286.58857.98850918982_calibrated.ms'


Stoke = 'I'

image_name= threedigits + '-mosaic-fieldAll-Stokes'+str(Stoke)+'-2.5arc-'+str(nit)+'-'+str(thresh)+'-spw16-pb'+str(pblim)+'-cyclenit500'

if os.path.exists(path+"/Images/"+image_name+".image.fits"):
    os.remove(path+"/Images/"+image_name+".image.fits")

flist = glob(path+'/Images/'+image_name)
for images in flist:
    shutil.rmtree(images)


tclean(vis=msfilename,
       field="PER_FIELD_*",
       spw="16",
       timerange="",
       uvrange="",
       antenna="",
       observation="",
       intent="",
       datacolumn="corrected",
       imagename=path+"/Images/"+image_name,
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

