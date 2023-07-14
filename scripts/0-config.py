#to run this script, you need to put your data in a directory named 'data' and put the script inside another directory named 'scripts'
#
import os
import sys
import tarfile
import shutil

# working_directory = sys.argv[1]
working_directory = '../data'

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


def unzip(path: str, endswith: str = ".tar") -> None:
    """
    Unzips the tar file including products

    path (str): The path of ms file which we want to find the tar file
    endswith (str): The ending of the tar file
    """
    for file in os.listdir(path):
        if file.endswith(endswith):
            tarfile_path = os.path.join(path, file)
            with tarfile.open(tarfile_path) as tar:
                tar.extractall(path=path) # specify which folder to extract to



def copy(directory='.', startswith='19B-053', endswith='.ms'):
    """
    Copy the ms file to the products directory

    directory (str): The directory which contains the ms file
    startswith (str): The starting of the ms file
    endswith (str): The ending of the ms file

    returns:
    copy of the ms file to the products directory
    """
    file = find_ms_folder(directory, startswith, endswith)
    print(file)
    splitted_path = file[0].split('/')
    destination = splitted_path[0]+'/'+splitted_path[1]+'/'+splitted_path[2]+'/products/'+splitted_path[3]
    return shutil.copytree(file[0], destination)


def find_tables(table_kind: str, directory="."):
    """
    finds tables.

    table_kind (str): name of the table
    directory (str): the directory which we will search for tables

    Returns:
    str: the full path and name of the table
    """
    for file in os.listdir(directory):
        if file.endswith(table_kind + ".tbl"):
            return(os.path.join(directory, file))


def table_list():
    """
    Makes a list of tables in order 

    Returns:
    str: the list of tables
    """
    table_lists = []
    table_lists.extend(
        [find_tables('gc'), 
        find_tables('opac'),
        find_tables('rq'),
        find_tables('finaldelay'), 
        find_tables('finalBPcal'), 
        find_tables('averagephasegain'), 
        find_tables('finalampgaincal'), 
        find_tables('finalphasegaincal')]
        )
    return table_lists    

#-----------------------------------------------------------------------------------------
folders_list = find_ms_folder(working_directory, "19B-053")

print('List of the folders:')
print(folders_list)

#-----------------------------------------------------------------------------------------
ms_folder = input('Which file do you want to continue with?\n')
#------------------------------------------------------------------------------------------

#unzipping the products folder
unzip(path=ms_folder, endswith=".tar")
print('Unzipping the tar file is done!')   

#unzippng the tables 
unzip(ms_folder + '/products', ".caltables.tgz")
print('Unzipping tables is done!')

#copy the ms file and its flagversion to products folder    
copy(directory=ms_folder,startswith='19B-053',endswith='.ms')
print('ms file copied to products')
copy(directory=ms_folder,startswith='19B-053',endswith='.ms.flagversions')
print('flagversions copied to products')

#------------------------------------------------------------------------------------------

filename = find_ms_folder(ms_folder+ '/products/', '19', '.ms')
filename = filename[0]

path = '../data/'+ ms_folder + '/products/'
msfilename = path + filename