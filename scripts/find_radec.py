import os
import time
import numpy as np

working_directory = '../data_new/'

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

def append_to_text_file(output_file, ra_dec_array):
    np.savetxt(output_file, np.array(ra_dec_array).T, delimiter='\t', fmt="%s")

############################################################

def most_recent_listobs(file_path):
    with open(file_path, 'r') as log_file:
        lines = log_file.readlines()

    line_index_list = []
    for idx, line in enumerate(lines):
        if "ID" in line and "RA" in line and "Decl" in line:
            line_index_list.append(idx)
    print('Number of listobs= ', len(line_index_list))
    line_index = max(line_index_list)
    print('index of RA and Dec line= ', line_index)

    return line_index

############################################################

def read_log_file(file_path, line_index):
    with open(file_path, 'r') as log_file:
        lines = log_file.readlines()
        target_lines= lines[line_index+4:line_index+59]

    ID = []
    ra = []
    dec = []
    for line in target_lines:
        items = line.split()
        ID.append(items[4])
        ra.append(items[7])
        dec.append(items[8])
    results = [ID, ra, dec]
    return results     
############################################################
# line_index = most_recent_listobs('./casa-20230721-224817.log')
# ra_dec_results = read_log_file('./casa-20230721-224817.log', line_index)
# append_to_text_file('./1.txt', ra_dec_results)

############################################################

log_file_name = get_most_recent_log('./')
print(log_file_name)



############################################################        
mslist = find_ms_folder (working_directory, startswith='19B-053', endswith='')
print(mslist)


for msfolder in mslist:
    line_index = []
    msfile = find_ms_folder(msfolder, '19', '.ms')
    msfile = msfile[0]
    print(msfile)
    listobs(msfile)

    log_file_name = get_most_recent_log('./')
    print(log_file_name)

    line_index = most_recent_listobs(log_file_name)
    ra_dec_results = read_log_file(log_file_name, line_index)
    append_to_text_file('./phasecenter/'+str(msfolder.split('/')[-1])+'_radecs.txt', ra_dec_results)

