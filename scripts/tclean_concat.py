import sys
sys.path.append('.')
import shutil
import os
from glob import glob

path = '../data/concat'
msfilename = path + '/546_775.ms'


pblim = 0.06
nit = 5000
Stoke = 'I'
thresh='1e-4'
phase_center='J2000 03:32:04.530001 +31.05.04.00000'

imagename = '546_775'+'mosaic-fieldAll-Stokes'+str(Stoke)+'-2.5arc-'+str(nit)+'-'+str(thresh)+'-spwAll-pb'+str(pblim)+'-cyclenit500'


tclean(vis=msfilename,
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
       nsigma=0,
       cycleniter=500,
       cyclefactor=1,
       restart=True,
       calcres=True,
       calcpsf=True,
       parallel=False,
       interactive=False)

exportfits(path+"/Images/"+imagename+".image", path+"/Images/"+imagename+".image.fits")

