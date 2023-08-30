import sys
sys.path.append('.')
from configs import path, phase_center, nit, thresh, threedigits
import shutil
import os
from glob import glob

filename = path+'/targets.ms'

pblim = 0.06

Stoke = 'I'

print('number of iterations is: ' + str(nit))
print('threshold is '   + str(thresh))


imagename= threedigits + '-awproject-fieldAll-Stokes'+str(Stoke)+'-2.5arc-'+str(nit)+'-'+str(thresh)+'-spwALL-pb'+str(pblim)+'-nsigma3'

if os.path.exists(path+"/Images/"+imagename+".image.fits"):
    os.remove(path+"/Images/"+imagename+".image.fits")

flist = glob(path+'/Images/'+imagename)
for images in flist:
    shutil.rmtree(images)


tclean(vis=filename,
       selectdata=True,
       field='',
       spw='',
       timerange='',
       uvrange='',
       antenna='',
       scan='',
       observation='',
       intent='',
       datacolumn='corrected',
       imagename=path+"/Images/"+imagename,
       imsize=4096,
       cell=2.5,
       phasecenter=phase_center,
       stokes=Stoke,
       projection='SIN',
       startmodel='',
       specmode='mfs',
       reffreq='',
       nchan=-1,
       start='',
       width='',
       outframe='LSRK',
       veltype='radio',
       restfreq=[],
       interpolation='linear',
       perchanweightdensity=True,
       gridder='awproject',
       facets=1,
       psfphasecenter='',
       wprojplanes=1,
       vptable='',
       mosweight=True,
       aterm=True,
       psterm=False,
       wbawp=False,
       conjbeams=False,
    #    cfcache='test.cf',
       usepointing=False,
       computepastep=360.0,
       rotatepastep=5.0,
       pointingoffsetsigdev=[],
       pblimit=pblim,
       normtype='flatnoise',
       deconvolver='hogbom',
       scales=[],
       nterms=2,
       smallscalebias=0.0,
       fusedthreshold=0.0,
       largestscale=-1,
       restoration=True,
       restoringbeam=[],
       pbcor=True,
       outlierfile='',
       weighting='briggs',
       robust=0.5,
       noise='1.0Jy',
       npixels=0,
       uvtaper=[],
       niter=nit,
       gain=0.1,
       threshold=thresh,
       nsigma=3,
       cycleniter=-1,
       cyclefactor=1.0,
       minpsffraction=0.05,
       maxpsffraction=0.8,
       interactive=False,
    #    fullsummary=False,
       nmajor=-1,
       usemask='user',
       mask='',
       pbmask=0.0,
       sidelobethreshold=3.0,
       noisethreshold=5.0,
       lownoisethreshold=1.5,
       negativethreshold=0.0,
       smoothfactor=1.0,
       minbeamfrac=0.3,
       cutthreshold=0.01,
       growiterations=75,
       dogrowprune=True,
       minpercentchange=-1.0,
       verbose=False,
       fastnoise=True,
       restart=True,
       savemodel='none',
       calcres=True,
       calcpsf=True,
       psfcutoff=0.35,
       parallel=False )

exportfits(path+"/Images/"+imagename+".image", path+"/Images/"+imagename+".image.fits")


#cycleniter
#normtype=pbsquare
#cyclefactor