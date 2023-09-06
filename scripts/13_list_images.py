import sys
sys.path.append('.')
from configs import path, thresh, nit, threedigits
import numpy as np

spw = [9,10,11,12,13,14,15,16,17,0,1,2,3,4,5,6,7,8]
existing_spw = [0, 2, 3 , 4, 5, 6, 8, 10, 15, 16, 17]
non_spw = [1, 7, 9, 11, 12, 13, 14]
channels = ['00~07', '08~15', '16~23', '24~31', '32~39', '40~47', '48~55', '56~63']

stokes = [
        'I',
        'Q',
        'U'
          ]

for stok in stokes:
    files_list = []
    for s in spw:
        for channel in channels:
            if s in existing_spw:
                files_list.append(path+"/Images/img"+str(nit)+"/fits/"+threedigits+"-spw"+str(s)+'-'+ str(channel)+"-2.5arcsec-nit"+str(nit)+"-"+str(thresh)+"-"+str(stok)+'.image.smo.fits')
            elif s in non_spw:
                files_list.append(path+"/Images/img"+str(nit)+"/fits/empty_channel.fits")    
        
    np.savetxt(path+'/Images/img'+str(nit)+'/stokes' + str(stok) +'.txt', files_list, fmt ='%s')            
            