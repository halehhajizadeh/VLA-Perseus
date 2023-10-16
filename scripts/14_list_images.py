import sys
sys.path.append('.')
from configs import path, thresh, nit, threedigits
import numpy as np
import os 

file_list = [file for file in os.listdir(path+"/Images/img"+str(nit)+"/fits/") if os.path.isfile(os.path.join(path+"/Images/img"+str(nit)+"/fits/", file))]
file_list_total = []
for file in file_list:
    file = path+"/Images/img"+str(nit)+"/fits/" + file 
    file_list_total.append(file)
print (file_list_total)

spw = [9,10,11,12,13,14,15,16,17,0,1,2,3,4,5,6,7,8]
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
            file_name = path+"/Images/img"+str(nit)+"/fits/"+threedigits+"-spw"+str(s)+'-'+ str(channel)+"-2.5arcsec-nit"+str(nit)+"-"+str(thresh)+"-"+str(stok)+'.image.smo.fits'
            if file_name in file_list_total:
                files_list.append(file_name)
            elif file_name not in file_list_total:
                files_list.append(path+"/Images/img"+str(nit)+"/fits/empty_channel.fits")    
        
    np.savetxt(path+'/Images/img'+str(nit)+'/stokes' + str(stok) +'.txt', files_list, fmt ='%s')            
            