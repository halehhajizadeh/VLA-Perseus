import sys
sys.path.append('.')
import shutil
import os
from glob import glob
# from configs import path, phase_center, nit, thresh, threedigits, msfilename

path = '../data'
phase_center = 'J2000 03:34:30.000000 +31.59.59.99999'
thresh = '2e-3'
nit = 10
threedigits = '03:34:30.000000_+31.59.59.99999'
pblim = 0.06

# path = '../data/19B-053_2020_01_09_T02_00_58.482/products'
# filename = path + '/19B-053.sb37665557.eb37682286.58857.98850918982_calibrated.ms'

mslist = ['../data/19B-053_2020_01_05_T00_25_02.102/19B-053.sb37659292.eb37664379.58853.92688378472.ms/',
          '../data/19B-053_2020_01_11_T23_24_56.263/19B-053.sb37659292.eb37692509.58859.886421828705.ms/',
          '../data/19B-053_2020_01_19_T02_24_58.208/19B-053.sb37659292.eb37728757.58867.005418773144.ms/',
          '../data/19B-053_2020_01_21_T08_37_05.970/19B-053.sb37659292.eb37739287.58869.013119236115.ms/',
          '../data/19B-053_2020_01_25_T22_36_59.587/19B-053.sb37747015.eb37783660.58873.84837011574.ms/'
          ]

Stoke = 'I'

image_name= threedigits + '-mosaic-fieldAll-Stokes'+str(Stoke)+'-2.5arc-'+str(nit)+'-'+str(thresh)+'-spw16-pb'+str(pblim)+'phase_field'


tclean(vis=mslist,
       field="J0336+3218",
       spw="16",
       timerange="",
       uvrange="",
       antenna="",
       observation="",
       intent="",
       datacolumn="corrected",
       imagename=path+"/Images/"+image_name,
       imsize=[3000],
       cell=2.5,
       phasecenter=phase_center,
       stokes=Stoke,
       projection="SIN",
       specmode="mfs",
       gridder="standard",
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
       # cycleniter=500,
       cyclefactor=1,
       restart=True,
       calcres=True,
       calcpsf=True,
       parallel=False,
       interactive=False)

exportfits(path+"/Images/"+image_name+".image", path+"/Images/"+image_name+".image.fits")

