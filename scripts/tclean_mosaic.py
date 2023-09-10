import sys
sys.path.append('.')
import shutil
import os
from glob import glob
from configs import path, phase_center, nit, thresh, threedigits

# path = '../data/19B-053_2019_12_16_T08_12_56.775/products'
# msfilename = path + '/19B-053.sb37264871.eb37596495.58833.2500384375_calibrated.ms'

filename = path+'/targets.ms'

pblim = 0.06

Stoke = 'I'

imagename= threedigits + '-mosaic-fieldAll-Stokes'+str(Stoke)+'-2.5arc-'+str(nit)+'-'+str(thresh)+'-spwALL-pb'+str(pblim)+'-cyclenit500'

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
       imsize=[4096],
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
       cyclefactor=1.5,
       restart=True,
       calcres=True,
       calcpsf=True,
       parallel=False,
       interactive=False)

exportfits(path+"/Images/"+imagename+".image", path+"/Images/"+imagename+".image.fits")

