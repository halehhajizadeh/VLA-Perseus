import sys
sys.path.append('.')
from configs import path, thresh, nit, threedigits
import time

spw = [2, 3 , 4, 5, 6, 8, 10, 15, 16, 17]

stokes = [
        'I',
        'Q',
        'U'
          ]
channels = [
    '00~07',
    '08~15', 
    '16~23', 
    '24~31', 
    '32~39', 
    '40~47', 
    '48~55', 
    '56~63'
    ]


tic = time.time()
for stok in stokes:
    for s in spw:
        for channel in channels:  
            imsmooth(imagename = path+"/Images/img"+str(nit)+"/tclean/"+threedigits+"-spw"+str(s)+'-'+ str(channel)+"-2.5arcsec-nit"+str(nit)+"-"+str(thresh)+"-"+str(stok)+'.image',
                    targetres = True,
                    major = '65arcsec',
                    minor ='50arcsec',
                    pa='0.0deg',
                    outfile = path+"/Images/img"+str(nit)+"/smo/"+threedigits+"-spw"+str(s)+'-'+ str(channel)+"-2.5arcsec-nit"+str(nit)+"-"+str(thresh)+"-"+str(stok)+'.image.smo',
                    overwrite=True
                    )
toc = time.time()
print(f"Finshed the smoothing process in {round((toc-tic)/60)} minutes")                
