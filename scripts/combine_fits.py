import astropy
from astropy.io import fits
import os
import numpy as np



working_directory = '../data_new/'
# working_directory = '../data/'

def find_ms_folder(directory, startswith='19B-053', endswith=''):
    """
    Finds names of ms files in a directroy.

    directory (str): The directory to search
    startswith (str): The beginning of the file to searchs
    endswith (str): The end of the file to search

    Returns:
    str : An array including the name of the ms files found.
    """
    folders_list = []
    for file in os.listdir(directory):
        if file.startswith(startswith):
            if file.endswith(endswith):
                folders_list.append(os.path.join(directory, file))                
    return(folders_list)



mslist = find_ms_folder (working_directory, startswith='19B-053', endswith='')
print(mslist)


# List the paths of the FITS files you want to combine
fits_files = []
for msfolder in mslist:
    msfolder = msfolder.split('/')[0] + '/' + msfolder.split('/')[1] + '/Images/' + msfolder.split('/')[-1]
    msfolder = msfolder + '.image.fits'
    fits_files.append(msfolder)


print (fits_files)    

def combine_fits_files(input_files, output_file):
    # Create an empty list to store the data from each file
    data_list = []

    # Read data from each FITS file and store it in the data_list
    for file_path in input_files:
        with fits.open(file_path) as hdul:
            data_list.append(hdul[0].data)

    # Concatenate the data arrays along the specified axis (0 for rows, 1 for columns)
    combined_data = np.concatenate(data_list, axis=0)

    # Create a new PrimaryHDU object with the combined data
    combined_hdu = fits.PrimaryHDU(combined_data)

    # Write the combined data to a new FITS file
    combined_hdu.writeto(output_file, overwrite=True)



# Define the output file path for the combined FITS file
output_file_path = working_directory+"Images/combined_file.fits"

# Call the combine_fits_files function to combine the FITS files
combine_fits_files(fits_files, output_file_path)

print("FITS files combined and saved as:", output_file_path)