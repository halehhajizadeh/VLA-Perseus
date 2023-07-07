import shutil
import os
from glob import glob

# path = '../data/19B-053_2020_01_03_T03_00_57.672/products/'
path = '../data/19B-053_2019_12_15_T07_36_56.546/products'
filename = path+'/targets.ms'

for i in range(55):
    imagename= '546-standard-field'+str(i)+'-5arc-10000-spw16'

    if os.path.exists(path+"/Images_new/"+imagename+".image.fits"):
        os.remove(path+"/Images_new/"+imagename+".image.fits")

    flist = glob(path+'/Images_new/'+imagename)
    for images in flist:
        shutil.rmtree(images)


    tclean(vis=filename,
        field=str(i),
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
        gridder="standard",
        mosweight=True,
        cfcache="",
        pblimit=0.1,
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
