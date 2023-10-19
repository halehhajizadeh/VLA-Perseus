import sys
sys.path.append('.')
import shutil
import os
from glob import glob

path = '../data/concat/03:32:04.530001_+31.05.04.00000/'
msfilename = path + 'J2000_03:32:04.530001_+31.05.04.00000.ms'


pblim = 0.06
nit = 5000
Stoke = 'I'
thresh='1e-4'
phase_center='J2000 03:32:04.530001 +31.05.04.00000'

imagename = 'original-'+'mosaic-fieldAll-Stokes'+str(Stoke)+'-2.5arc-'+str(nit)+'-'+str(thresh)+'-spw16-pb'+str(pblim)+'-cyclenit500'


tclean(vis=msfilename,
       field="PER_FIELD_*",
       spw="16:5~60",
       timerange="",
       uvrange="",
       antenna="",
       observation="",
       intent="",
       datacolumn="corrected",
       imagename=path+imagename,
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

exportfits(path+imagename+".image", path+imagename+".image.fits")

