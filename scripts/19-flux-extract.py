import sys
sys.path.append('.')
from configs import path, nit, threedigits, thresh
import numpy as np
from astropy.io import fits
from astropy.wcs import WCS
import math
import pandas as pd

pblim = 0.06

dx=4
dy=4


deltax = 10
deltay = 10
deltaxy = 7


Stokes = [
        'I',
        'Q',
        'U'
        ]

manual_setting=1


def ra_dec_to_degrees(ra, dec):
    ra = ra.split(':')
    ra_hours = int(ra[0])
    ra_minutes = int(ra[1])
    ra_seconds = int(ra[2])

    dec = dec.split(':')
    dec_degrees = int(dec[0])
    dec_minutes = int(dec[1])
    dec_seconds = int(dec[2])
    # Convert RA to degrees
    ra_degrees = (ra_hours + ra_minutes / 60 + ra_seconds / 3600) * 15

    # Convert Dec to degrees
    sign = 1 if dec_degrees >= 0 else -1
    dec_degrees = abs(dec_degrees) + dec_minutes / 60 + dec_seconds / 3600
    dec_degrees *= sign

    return ra_degrees, dec_degrees

#----------------------------------------------------------------
if manual_setting == 1:
    ra_list = ['3:31:54', '3:34:16', '3:33:21', '3:35:05', '3:31:19', '3:30:09', '3:28:40', '3:32:41', '3:34:01']
    dec_list = ['31:04:39', '31:12:10', '30:55:28', '30:47:04', '30:47:23', '30:32:53', '30:49:56', '30:20:11', '31:18:40']

    ra_list = np.array(ra_list)
    dec_list = np.array(dec_list)

    RA0=[]
    DEC0=[]
    for i in range(ra_list.shape[0]):
        radec=ra_dec_to_degrees(ra_list[i], dec_list[i])
        RA0.append(radec[0])
        DEC0.append(radec[1])


elif manual_setting == 0:   

    imagename= threedigits + '-mosaic-fieldALL-Stokes'+str(Stoke)+'-2.5arc-'+str(nit)+'-'+str(thresh)+'-spwALL-pb'+str(pblim)+'-cyclenit500'

    catalog_name= path +'/Images/'+ imagename + '.image.pybdsf.srl'

    df = pd.read_csv(catalog_name, delim_whitespace=True)

    RA0 = df['RA'].tolist()
    DEC0 = df['DEC'].tolist()
#----------------------------------------------------------------
for stokes in Stokes:
    
    fits_file =path+'/Images/img'+str(nit)+'/Stokes'+stokes+'.fits'
    hdulist=fits.open(fits_file)
    img=hdulist[0].data
    wcs=WCS(hdulist[0].header)
    
    if stokes=='I':
        stok = 1
    if stokes=='Q':
        stok = 2
    if stokes=='U':
        stok = 3        

    for ip in range(len(RA0)):
        sky1=[[RA0[ip],DEC0[ip],1.47339395E9,0]]
        pixcrd2 = wcs.all_world2pix(sky1, 0) 
        print(pixcrd2)

        x0=int(pixcrd2[0][0]+0.5)
        y0=int(pixcrd2[0][1]+0.5)

        if (DEC0[ip]>=0):
            sourcename_RADEC="H%07.3f+%06.3f"  % (int(1.E3*RA0[ip])/1000.,int(1.E3*DEC0[ip])/1000.)
        else:  
            sourcename_RADEC="H%07.3f%06.3f"  % (int(1.E3*RA0[ip])/1000.,int(1.E3*DEC0[ip])/1000.)

        spectrum_file = "%s_%s_%s_%s.pro" % (sourcename_RADEC, dx, dy, stokes)

        OUT=open(path+'/Images/img'+str(nit)+'/RMsyn/'+spectrum_file,"w")

        print("Pixel coordinates: ",x0,y0,sourcename_RADEC,spectrum_file)
        print("## RA DEC: ",RA0[ip],DEC0[ip], file=OUT)
        print("## Pixel coordinates: ",x0,y0,"  Box : %d  %d" % (dx,dy), file=OUT)
        print("## Source name: ",sourcename_RADEC," Stokes ",stokes, file=OUT)
        print("## Spectrum file: ",spectrum_file, file=OUT)
        print("##  ", file=OUT)

        box_spectrum=img[:,(y0-dy):(y0+dy),(x0-dx):(x0+dx)]
        mean_spectrum=img[:,x0,y0]
        freq=np.copy(mean_spectrum)
        

        # Use the array flag to keep track of flagged channels
        flag=np.copy(mean_spectrum)*0.0

        flag[np.isnan(flag)]=0.0

       
        for ispec in range(len(mean_spectrum)):
            # Get ferquency of channel:
            # I have to change th 4th index
            sky=wcs.all_pix2world([[x0,y0,ispec,stok]],0)
            freq[ispec]=sky[0][2]

            # Average over the box:
            mean_spectrum[ispec]=np.average(box_spectrum[ispec,:,:])
            
            
            #Background
            background_1 = img[ispec,x0, (y0+deltay)]
            background_2 = img[ispec,x0, (y0-deltay)]
            background_3 = img[ispec,(x0+deltax), y0]
            background_4 = img[ispec,(x0-deltax), y0]
            background_5 = img[ispec,(x0+deltax), (y0+deltay)]
            background_6 = img[ispec,(x0+deltax), (y0-deltay)]
            background_7 = img[ispec,(x0-deltax), (y0-deltay)]
            background_8 = img[ispec,(x0-deltax), (y0+deltay)]
            print (f"Backgrounds:{background_1},{background_2},{background_3},{background_4},{background_5},{background_6},{background_7},{background_8}")
            
            diff = mean_spectrum[ispec]-[background_1,background_2,background_3,background_4,
                    background_5,background_6,background_7,background_8]
            
            mean_spectrum_reduced = np.median(diff)
            
            if (mean_spectrum[ispec]>1.E10):
                # If in here, found at least some pixels with BLANK vale 1.E30
                # Discard the whole channel. Set flag array value to 1.
                mean_spectrum[ispec]=0
                flag[ispec]=1.
            print("%15.12e  %15.8e  %d" % (freq[ispec],mean_spectrum_reduced,int(flag[ispec]+0.5)), file=OUT)


        OUT.close()

    rms=np.std(mean_spectrum)

    if (rms>0.002):
        print(sourcename_RADEC, rms)