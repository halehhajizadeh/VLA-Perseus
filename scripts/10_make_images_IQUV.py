import sys
sys.path.append('.')
from configs import path, phase_center, thresh, nit, threedigits, pblim, spw
import time

filename = path+'/targets.ms'

channels = ['00~07', '08~15', '16~23', '24~31', '32~39', '40~47', '48~55', '56~63']

for s in spw:
    for channel in channels:
        tic = time.time()
        print(f"stokes: IQU, s: {s}, channel: {channel} is started ...")
        tclean( vis=filename,
                field="",
                spw=str(s) + ':' + channel,
                timerange="",
                uvrange="",
                antenna="",
                observation="",
                intent="",
                datacolumn="corrected",
                imagename=path+"/Images/img"+str(nit)+"/tclean/"+str(threedigits)+"-spw"+str(s)+'-'+ str(channel)+"-2.5arcsec-nit"+str(nit)+"-"+str(thresh)+"-IQUV",
                imsize=[4320],
                cell='2.5arcsec',
                phasecenter=phase_center,
                stokes="IQUV",
                projection="SIN",
                specmode="mfs",
                gridder="awproject",
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
                psfcutoff=0.35,
                threshold=thresh,
                nsigma=0,
                cycleniter=-1,
                cyclefactor=1,
                restart=True,
                calcres=True,
                wbawp=False,
                calcpsf=True,
                parallel=True,
                verbose=True,
                wprojplanes=32,
                psterm=False,
                conjbeams=False,
                aterm=True)
    
        toc = time.time()
        print(f"stokes: IQUV, s: {s}, channel: {channel} is finished!")
        print(f"Finshed the process in {round((toc-tic)/60)} minutes")
