# First index is Stokes
# Second index is frequency
# Third index is DEC
# Fourth index is RA
import sys
sys.path.append('.')
from configs import path, nit

import numpy as np
from astropy.io import fits


stokes_list = [
        'I',
        'Q',
        'U'
          ]

def create_empty_channel(fitsname):
    flagged_channel = path+'/Images/img'+str(nit)+'/fits/empty_channel.fits'
    syscommand='rm -rf '+flagged_channel
    os.system(syscommand)
    hdul = fits.open(fitsname)
    img_fits = hdul[0].data
    header_fits = hdul[0].header
    img_fits[:] = np.nan
    cube_fits = np.copy(img_fits[0,:,:,:])
    flagged=np.copy(img_fits)
    hdul[0].data=flagged
    return hdul.writeto(flagged_channel)

def remove_empty_channel_form_start(filelist):
    if len(filelist) <= 0:
        return []
    if not "empty_channel.fits" in filelist[0]:
        return filelist
    else:
        return remove_empty_channel_form_start(filelist[1:])
    
for stokes in stokes_list:    
    cubename=path+'/Images/img'+str(nit)+'/Stokes'+stokes+'.fits'

    syscommand='rm -rf '+cubename
    os.system(syscommand)
    with open(path+'/Images/img'+str(nit)+'/stokes'+stokes+'.txt', 'r') as f:
        file_list = f.read().splitlines()

    file_list = remove_empty_channel_form_start(filelist=file_list)

    # Adding the first channel to the list
    inputfile = file_list[0]
    hdulist=fits.open(inputfile)
    img=hdulist[0].data
    header=hdulist[0].header
    cube=np.copy(img[0,:,:,:])


    #Define empty channel:
    create_empty_channel(inputfile)
    print('empty channel is produced!')


    # Loop through the file list and open each fits file in order
    for filename in file_list:
        with fits.open(filename) as hdulistCP:
            imgCP = hdulistCP[0].data      
            headerCP = hdulistCP[0].header
            # print(filename)
            if filename == path+'/Images/img' + str(nit) + '/fits/empty_channel.fits':
                imgCP = np.nan_to_num(x=imgCP, nan=1e30)
            img2cube=np.copy(imgCP[0,:,:,:])
            cube=np.append(cube,img2cube,0)

    print('for loop completed!')

    hdulist[0].data=cube
    hdulist.writeto(cubename)

    print('making cube is done!')