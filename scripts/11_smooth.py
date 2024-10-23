import sys
sys.path.append('.')
import time
import os

nit=5000
thresh = '2e-4'

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

# specific_dirs = '03:32:04.530001_+31.05.04.00000/'
specific_dirs =  '03:36:00.000000_+30.30.00.00001/' 
# specific_dirs =  '03:34:30.000000_+31.59.59.99999/'
# specific_dirs =  '03:25:30.000000_+29.29.59.99999/'
# specific_dirs =  '03:23:30.000001_+31.30.00.00000/'


tic = time.time()
for stok in stokes:
    for s in spw:
        for channel in channels:  

            image_name =  os.path.join("../data/concat/", specific_dirs, "Images/img" + str(nit) + "/tclean/", "spw" + str(s) + '-' + str(channel) + "-2.5arcsec-nit" + str(nit) + "-" + str(thresh) + "-" + str(stok)) + ".image"
            smo_image_name =  os.path.join("../data/concat/", specific_dirs, "Images/img" + str(nit) + "/smo", "spw" + str(s) + '-' + str(channel) + "-2.5arcsec-nit" + str(nit) + "-" + str(thresh) + "-" + str(stok)) +'.image.smo'

            print(smo_image_name)


            imsmooth(imagename = image_name,
                    targetres = True,
                    major = '80arcsec',
                    minor ='70arcsec',
                    pa='0.0deg',
                    outfile = smo_image_name,
                    overwrite=True
                    )
toc = time.time()
print(f"Finshed the smoothing process in {round((toc-tic)/60)} minutes")                

