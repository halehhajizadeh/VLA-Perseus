import sys
sys.path.append('.')
import time
import os

path='../data/concat/03:32:04.530001_+31.05.04.00000'
filename = path+'/J2000_03:32:04.530001_+31.05.04.00000.ms'
spw = [ 2, 3 , 4, 5, 6, 8, 15, 16, 17]
stokes1 = [
        'I',
        'Q',
        'U'
          ]
phase_center = 'J2000 03:32:04.530001 +31.05.04.00000'
threedigits = '03:32:04.530001_+31.05.04.00000'
thresh = '1e-4'
nit = 5000
pblim = 0.06


channels = ['00~07', '08~15', '16~23', '24~31', '32~39', '40~47', '48~55', '56~63']

for stok in stokes1:
    for s in spw:
        for channel in channels:
            tic = time.time()
            print(f"stokes: {stok}, s: {s}, channel: {channel} is started ...")

            img_filename = path + "/Images/img" + str(nit) + "/tclean/" + str(threedigits) + "-spw" + str(s) + '-' + str(channel) + "-2.5arcsec-nit" + str(nit) + "-" + str(thresh) + "-" + str(stok)

            if os.path.exists(img_filename):
                print(f"stokes: {stok}, s: {s}, channel: {channel} image already exists, skipping...")
                continue

            tclean( vis=filename,
                    field="",
                    spw=str(s) + ':' + channel,
                    timerange="",
                    uvrange="",
                    antenna="",
                    observation="",
                    intent="",
                    datacolumn="corrected",
                    imagename=img_filename,
                    imsize=[4320],
                    cell=2.5,
                    phasecenter=phase_center,
                    stokes=stok,
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
                    niter=nit,
                    gain=0.1,
                    threshold=thresh,
                    nsigma=0,
                    cycleniter=500,
                    cyclefactor=1,
                    parallel=False)
        
            toc = time.time()
            print(f"stokes: {stok}, s: {s}, channel: {channel} is finished!")
            print(f"Finshed the process in {round((toc-tic)/60)} minutes")