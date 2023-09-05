import sys
sys.path.append('.')
from configs import path, thresh, nit, threedigits
import time

spw = [0, 2, 3 , 4, 5, 6, 8, 10, 15, 16, 17]
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
    '56~63']

tic = time.time()
for stok in stokes:
    for s in spw:
        for channel in channels:
            exportfits(
                imagename = path+"/Images/img"+str(nit)+"/smo/"+threedigits+"-spw"+str(s)+'-'+ str(channel)+"-2.5arcsec-nit"+str(nit)+"-"+str(thresh)+"-"+str(stok)+'.image.smo',
                fitsimage = path+"/Images/img"+str(nit)+"/fits/"+threedigits+"-spw"+str(s)+'-'+ str(channel)+"-2.5arcsec-nit"+str(nit)+"-"+str(thresh)+"-"+str(stok)+'.image.smo.fits'
            )

toc = time.time()
print(f"Finshed the exporting process in {round((toc-tic)/60)} minutes")       


