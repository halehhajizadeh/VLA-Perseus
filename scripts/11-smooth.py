import time
path = '../data/19B-053_2019_12_15_T07_36_56.546/products/'
spw = [0, 2, 3 , 4, 5, 6, 8, 15, 16, 17]

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
thresh = '1e-4'
nit = 20000

tic = time.time()
for stok in stokes:
    for s in spw:
        for channel in channels:  # JAVAD: in below because of error, I changed the "./Images" to "Images"
            imsmooth(imagename = path+"Images/img"+str(nit)+"/tclean/546-spw"+str(s)+'-'+ str(channel)+"-2.5arcsec-nit"+str(nit)+"-"+str(thresh)+"-"+str(stok)+'.image',
                    targetres = True,
                    major = '55arcsec',
                    minor ='50arcsec',
                    pa='0.0deg',
                    outfile = path+"Images/img"+str(nit)+"/smo/546-spw"+str(s)+'-'+ str(channel)+"-2.5arcsec-nit"+str(nit)+"-"+str(thresh)+"-"+str(stok)+'.image.smo',
                    overwrite=True
                    )
toc = time.time()
print(f"Finshed the smoothing process in {round((toc-tic)/60)} minutes")                

