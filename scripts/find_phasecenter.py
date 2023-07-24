import os
import time

working_directory = '../data/'

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

###############################################################

def get_most_recent_log(directory):
    files = [file for file in os.listdir(directory) if (file.lower().endswith('.log'))]
    files.sort(key=os.path.getmtime)
    files = sorted(files,key=os.path.getmtime)

    if files: 
        return files[-1]
    else:
        return None

#############################################################

def append_to_text_file(output_file, nfield, ra, dec):
    with open(output_file, 'a') as file:
        file.write(f"{nfield}\t{ra}\t{dec}\n")

############################################################

def read_log_file(file_path):
    with open(file_path, 'r') as log_file:
        lines = log_file.readlines()

    results = []
    for line in lines:
        if "FieldName" in line and "RA" in line and "DEC" in line:
            items = line.split()
            field_name = items[4]
            ra = items[22]
            dec = items[23]
            results.append((field_name, ra, dec))
    
    return results        

############################################################

log_file_name = get_most_recent_log('./')
print(log_file_name)

############################################################

############################################################        
mslist = find_ms_folder (working_directory, startswith='19B-053', endswith='')
print(mslist)

for msfolder in mslist:
    msfile = find_ms_folder(msfolder, '19', '.ms')
    msfile = msfile[0]
    print(msfile)
    listobs(msfile)
