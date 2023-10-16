import os
import sys
import tarfile
import shutil


working_directory = '../data'
new_ms_name = 'J2000_03:32:04.530001_+31.05.04.00000'

def find_ms_folder(directory, startswith='19B-053', endswith=''):
    """
    Finds names of ms files in a directroy.

    directory (str): The directory to search
    startswith (str): The beginning of the file to search
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


folders_list = find_ms_folder(working_directory, "19B-053")

ms_list = []
for i in folders_list:
    ms_list.append(i+'/targets.ms')

print(ms_list)

concat(ms_list, concatvis=working_directory+'/'+new_ms_name+'.ms')


