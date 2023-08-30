import sys
sys.path.append('.')
from configs import path, phase_center, thresh, nit, threedigits
import time

filename = path+'/targets.ms'
spw = [0, 2, 3 , 4, 5, 6, 8, 10, 15, 16, 17]
stokes1 = [
        'I',
        'Q',
        'U'
          ]

channels = ['00~07', '08~15', '16~23', '24~31', '32~39', '40~47', '48~55', '56~63']

for stok in stokes1:
    for s in spw:
        for channel in channels:
            tic = time.time()
            print(f"stokes: {stok}, s: {s}, channel: {channel} is started ...")
            tclean(vis= filename,
                field="PER_FIELD_*",
                spw=str(s) + ':' + channel,
                timerange="",
                uvrange="",
                antenna="",
                scan="",
                observation="",
                intent="",
                datacolumn="corrected",
                imagename=path+"/Images/img"+str(nit)+"/tclean/"+str(threedigits)+"-spw"+str(s)+'-'+ str(channel)+"-2.5arcsec-nit"+str(nit)+"-"+str(thresh)+"-"+str(stok),
                imsize=[4320],
                cell="2.5arcsec",
                phasecenter= phase_center,
                stokes=stok,
                projection="SIN",
                specmode="mfs",
                outframe="LSRK",
                veltype="radio",
                restfreq=[],
                interpolation="linear",
                gridder="mosaic",
                mosweight=True,
                cfcache="",
                pblimit=0.01,
                normtype="flatnoise",
                deconvolver="hogbom",
                scales=[],
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
                savemodel="modelcolumn",
                calcres=True,
                calcpsf=True,
                parallel=False,
                interactive=False)
            toc = time.time()
            print(f"stokes: {stok}, s: {s}, channel: {channel} is finished!")
            print(f"Finshed the process in {round((toc-tic)/60)} minutes")
