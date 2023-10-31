import sys
sys.path.append('.')
from configs import path, thresh, nit, threedigits
import time

spw = [2, 3 , 4, 5, 6, 8, 15, 16, 17]

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

            # image_name = path+"/Images/img"+str(nit)+"/tclean/"+threedigits+"-spw"+str(s)+'-'+ str(channel)+"-2.5arcsec-nit"+str(nit)+"-"+str(thresh)+"-"+str(stok)+'.image',
            image_name =  path + "/concat/"+str(threedigits)+"/Images/img" + str(nit) + "/tclean/" + str(threedigits) + "-spw" + str(s) + '-' + str(channel) + "-2.5arcsec-nit" + str(nit) + "-" + str(thresh) + "-" + str(stok)+'.image'
            # smo_image_name = path+"/Images/img"+str(nit)+"/smo/"+threedigits+"-spw"+str(s)+'-'+ str(channel)+"-2.5arcsec-nit"+str(nit)+"-"+str(thresh)+"-"+str(stok)+'.image.smo',
            smo_image_name =  path + "/concat/"+str(threedigits)+"/Images/img" + str(nit) + "/smo/" + str(threedigits) + "-spw" + str(s) + '-' + str(channel) + "-2.5arcsec-nit" + str(nit) + "-" + str(thresh) + "-" + str(stok)+'.image.smo'

            imsmooth(imagename = image_name,
                    targetres = True,
                    major = '55arcsec',
                    minor ='45arcsec',
                    pa='0.0deg',
                    outfile = smo_image_name,
                    overwrite=True
                    )
toc = time.time()
print(f"Finshed the smoothing process in {round((toc-tic)/60)} minutes")                

